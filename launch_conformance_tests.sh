#!/bin/bash
#
# GEISA Conformance Launch script
# Copyright (C) 2025 Southern California Edison
#
# GEISA Conformance is free software, distributed under the Apache License
# version 2.0. See LICENSE for details.

RED="\e[31m"
ORANGE="\e[33m"
ENDCOLOR="\e[0m"

ABSOLUTE_PATH="$(readlink -f "$0")"
TOPDIR="$(dirname "${ABSOLUTE_PATH}")"
NO_REPORTS=false

source "${TOPDIR}"/src/launch_conformance_tests_ssh.sh

usage()
{
	cat <<EOF

GEISA Conformance Launch script

Usage: $0 [options]

Required options:
  --ip <board_ip>     Specify the IP address of the board to run tests on
or
  --serial <serial_port>  Specify the serial port of the board to run tests on

Optional options:
  --user <username>   Specify the username for SSH connection (default: root)
  --password <password>  Specify the password for SSH connection (default: empty)
  --no-reports        Do not generate test reports (only run tests and display results)
  --baudrate <baudrate> Specify the baudrate for the serial port of the board (default: 115200)
  --help              Show this help message
EOF
	exit 1
}

while [[ "$#" -gt 0 ]]; do
	case "$1" in
		--ip)
		BOARD_IP="$2"
		if [[ -z "${BOARD_IP}" ]]; then
			echo -e "${RED}Error:${ENDCOLOR} IP address cannot be empty"
			usage
		fi
		shift 2
		;;
		--serial)
		BOARD_SERIAL="$2"
		if [[ -z "${BOARD_SERIAL}" ]]; then
			echo -e "${RED}Error:${ENDCOLOR} Serial port cannot be empty"
			usage
		fi
		shift 2
		;;
		--user)
		BOARD_USER="$2"
		if [[ -z "${BOARD_USER}" ]]; then
			echo -e "${RED}Error:${ENDCOLOR} Username cannot be empty"
			usage
		fi
		shift 2
		;;
		--password)
		BOARD_PASSWORD="$2"
		if [[ -z "${BOARD_PASSWORD}" ]]; then
			echo -e "${RED}Error:${ENDCOLOR} Password cannot be empty"
			usage
		fi
		shift 2
		;;
		--no-reports)
		NO_REPORTS=true
		shift
		;;
		--baudrate)
		BAUDRATE="$2"
		if [[ -z "${BAUDRATE}" ]]; then
			echo -e "${RED}Error:${ENDCOLOR} Baudrate cannot be empty"
			usage
		fi
		shift 2
		;;
		--help)
		usage
		;;
		*)
		echo -e "${RED}Error:${ENDCOLOR} Unknown option '$1'"
		usage
		;;
	esac
done

if [[ -z ${BOARD_IP} && -z ${BOARD_SERIAL} ]]; then
	echo -e "${RED}Error:${ENDCOLOR} Board IP address or serial port is required."
	usage
fi

if [[ -n ${BOARD_IP} && -n ${BOARD_SERIAL} ]]; then
	echo -e "${ORANGE}Warning:${ENDCOLOR} Board IP address and serial port specified, launching test with ssh connection."
fi

if [[ -n ${BOARD_IP} ]]; then
	BOARD_USER=${BOARD_USER:-root}

	connect_and_transfer_with_ssh "${BOARD_IP}" "${BOARD_USER}" "${BOARD_PASSWORD}" "${TOPDIR}"
	if ! ${NO_REPORTS}; then
		launch_tests_with_report_ssh "${BOARD_IP}" "${BOARD_USER}" "${BOARD_PASSWORD}" "${TOPDIR}"
	else
		launch_tests_without_report_ssh "${BOARD_IP}" "${BOARD_USER}" "${BOARD_PASSWORD}"
	fi
	cleanup_ssh "${BOARD_IP}" "${BOARD_USER}" "${BOARD_PASSWORD}"
else
	echo "Starting GEISA Conformance Tests on board via ${BOARD_SERIAL}"
	args=(--serial "${BOARD_SERIAL}" \
		--user "${BOARD_USER:-root}" \
		--password "${BOARD_PASSWORD:-}" \
		--baudrate "${BAUDRATE:-115200}")
	if ${NO_REPORTS}; then
		args+=(--no-reports)
	fi
	python3 "${TOPDIR}"/src/launch_conformance_tests_serial.py "${args[@]}"
	test_exit_code=$?
	if [[ ${test_exit_code} -eq 255 ]]; then
		echo -e "${RED}Error:${ENDCOLOR} Failed to launch tests on board via serial port"
		exit "${test_exit_code}"
	fi

fi

if ! ${NO_REPORTS}; then
	echo "Generating PDF report"
	# shellcheck disable=SC2015
	cd "${TOPDIR}"/src/test-report-pdf && \
	./compile.py -i "${TOPDIR}"/reports/ -p 'GEISA conformance tests' -d "${TOPDIR}"/src/pdf_themes && \
	mv "${TOPDIR}"/src/test-report-pdf/test-report.pdf "${TOPDIR}"/reports/geisa-conformance-report.pdf || {
		echo -e "${RED}Error:${ENDCOLOR} Failed to create PDF report"
		exit 1
	}
	cd "${TOPDIR}" || exit 1
fi

exit "${test_exit_code}"
