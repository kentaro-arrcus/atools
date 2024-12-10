#!/usr/bin/bash

if [[ $(id -u) -ne 0 ]] ; then echo "Run with sudo" ; exit 1 ; fi

set -e

if [ -n "$SUDO_UID" ]; then
    uid=$SUDO_UID
else
    uid=$UID
fi

run () {
    echo "$@"
    "$@" || exit 1
}

silent () {
    "$@" 2> /dev/null || true
}

create_network () {
  run ip netns add ptf0
  run ip link add name veth10 type veth peer name veth11
  run ip link add name veth20 type veth peer name veth21
  run ip link set veth10 netns ptf0
  run ip link set veth20 netns ptf0

  run ip netns exec ptf0 ip link set dev lo up
  run ip netns exec ptf0 ethtool --offload veth10 rx off tx off
  run ip netns exec ptf0 ip addr add 10.0.10.10/24 dev veth10
  run ip netns exec ptf0 ip link set veth10 address 02:03:04:05:06:10
  run ip netns exec ptf0 ip link set dev veth10 up

  run ip netns exec ptf0 ip link set dev lo up
  run ip netns exec ptf0 ethtool --offload veth20 rx off tx off
  run ip netns exec ptf0 ip addr add 10.0.20.10/24 dev veth20
  run ip netns exec ptf0 ip link set veth20 address 02:03:04:05:06:20
  run ip netns exec ptf0 ip link set dev veth20 up

  run ethtool --offload veth11 rx off tx off
  run ip addr add 10.0.10.1/24 dev veth11
  run ip link set veth11 address 02:03:04:05:06:11
  run ip link set dev veth11 up

  run ethtool --offload veth21 rx off tx off
  run ip addr add 10.0.20.1/24 dev veth21
  run ip link set veth21 address 02:03:04:05:06:21
  run ip link set dev veth21 up
}

destroy_network () {
  echo "destroy_network"

  run ip netns del ptf0
  # veth are auto deleted
}

while getopts "cd" ARGS;
do
    case $ARGS in
    c ) create_network
        exit 1;;
    d ) destroy_network
        exit 1;;
    esac
done

echo "Usage: $0 -{c|d} (c: create, d:delete)"
cat << EOF
IPv4 and MAC address is statically configured.

  +-------------------+
  |       ptf0        |
  |                   |
  | (veth10) (veth20) |
  +-----|--------|----+
        |        |
    (veth11) (veth21)
  
  host (netns: default)
  
- veth10: 10.0.10.10/24 (02:03:04:05:06:10)
- veth20: 10.0.20.10/24 (02:03:04:05:06:20)
- veth11: 10.0.10.1/24  (02:03:04:05:06:11)
- veth21: 10.0.20.1/24  (02:03:04:05:06:21)
EOF