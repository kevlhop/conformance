/**
 * @file gapi_sensor.c
 * @brief Test sensor API messages
 * @copyright Copyright (C) 2026 Southern California Edison
 */
#include "gapi_discovery.h"
#include "geisa_status.h"
#include "pb.h"
#include "pb_decode.h"
#include "pb_encode.h"
#include "schemas/sensor.pb.h"

volatile bool running = true;
volatile bool isConnected = false;
volatile bool rr_disconnect = false;
const int TIMEOUT_S = 5;

/**
 * @brief Context structure for the sensor test, used to store
 * information about the device under test and the test result.
 */
struct sensor_test_ctx {
	int test_result;
	int sensors_count;
	GeisaSensorDescriptor *sensor;
};

/**
 * @brief Callback function to get the discovery information of the device under
 * test. This function decodes the discovery response and updates the context
 * with information about the device.
 *
 * @param mosq The mosquitto client instance
 * @param obj The user data object, which is a pointer to the sensor test
 * context
 * @param msg The MQTT message containing the discovery response
 */
static void get_discovery_information(struct mosquitto *mosq, void *obj,
				      const struct mosquitto_message *msg)
{
	GeisaPlatformDiscovery_Rsp response =
	    GeisaPlatformDiscovery_Rsp_init_default;
	struct sensor_test_ctx *ctx = obj;
	pb_istream_t istream;
	bool status = false;
	(void)mosq;

	ctx->sensors_count = 0;
	ctx->sensor = NULL;

	istream = pb_istream_from_buffer(msg->payload, msg->payloadlen);
	status =
	    pb_decode(&istream, GeisaPlatformDiscovery_Rsp_fields, &response);

	if (!status) {
		fprintf(stderr, "[Sensor] Error decoding discovery response\n");
		ctx->test_result = EXIT_FAILURE;
		goto disconnect;
	}

	if (!response.has_sensor) {
		goto disconnect;
	}

	ctx->sensors_count = response.sensor.sensors_count;
	ctx->sensor = calloc(ctx->sensors_count, sizeof(*ctx->sensor));
	if (!ctx->sensor) {
		fprintf(stderr,
			"[Sensor] Error allocating memory for streams\n");
		ctx->test_result = EXIT_FAILURE;
		goto disconnect;
	}

	// Shallow copy as no pointer members are present in the sensor
	// structure
	for (int i = 0; i < ctx->sensors_count; i++) {
		ctx->sensor[i] = response.sensor.sensors[i];
	}

disconnect:
	pb_release(GeisaPlatformDiscovery_Rsp_fields, &response);
	rr_disconnect = true;
}

/**
 * @brief Main function for sensor API tests, initializes MQTT communication,
 * sets appropriate message callback based on command line argument, sends
 * discovery request and sensor request to check sensor response message
 *
 * @param argc Argument count from command line
 * @param argv Argument vector from command line, expects one argument
 * specifying the callback type to test
 * @return EXIT_SUCCESS if all tests pass, EXIT_FAILURE if any test fails or if
 * there is an error in setup
 */
int main(int argc, char *argv[])
{
	GeisaSensorReadings_Req request = GeisaSensorReadings_Req_init_default;
	struct mosquitto *mosq = NULL;
	int return_code = 0;
	time_t start = 0;
	(void)argc;
	(void)argv;

	struct sensor_test_ctx *ctx = calloc(1, sizeof(struct sensor_test_ctx));
	if (!ctx) {
		fprintf(stderr,
			"Error allocating memory for sensor test context\n");
		return EXIT_FAILURE;
	}
	ctx->test_result = 0;

	mosq = api_communication_init();
	if (!mosq) {
		return_code = EXIT_FAILURE;
		goto exit;
	}

	mosquitto_user_data_set(mosq, ctx);

	start = time(NULL);
	while (running && !isConnected) {
		mosquitto_loop(mosq, -1, 1);
		if (difftime(time(NULL), start) > TIMEOUT_S) {
			fprintf(
			    stderr,
			    "[Sensor] Connection timed out after %d seconds\n",
			    TIMEOUT_S);
			return_code = EXIT_FAILURE;
			goto disconnect;
		}
	}

	if (!isConnected) {
		fprintf(stderr, "[Sensor] Failed to connect to broker\n");
		return_code = EXIT_FAILURE;
		goto disconnect;
	}

	mosquitto_message_callback_set(mosq, get_discovery_information);
	return_code = send_discovery_request(mosq);
	if (return_code != EXIT_SUCCESS) {
		fprintf(stderr, "[Sensor] Error sending discovery request\n");
		goto disconnect;
	}

	(void)request;

disconnect:
	api_communication_deinit(mosq);
exit:
	return_code = return_code ? return_code : ctx->test_result;
	free(ctx->sensor);
	free(ctx);
	return return_code;
}
