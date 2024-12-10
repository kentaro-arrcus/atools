# PTF Test for L3FW

This is an example of simple Layter 3 forwarding test using PTF.

Test items:

- IPv4
  - arp
  - ping (layer 3 forwarding)
  - TTL expired
- IPv6
  - TBD

## Topology

- Create netns `ptf0` as virtual host.
- Use host (netns:default) as DUT.

```topo
+-------------------+
|       ptf0        |
|                   |
| (veth10) (veth20) |
+-----|--------|----+
      |        |
  (veth11) (veth21)

host (netns: default)
```

- veth10: 10.0.10.10/24 (02:03:04:05:06:10)
- veth20: 10.0.20.10/24 (02:03:04:05:06:20)
- veth11: 10.0.10.1/24  (02:03:04:05:06:11)
- veth21: 10.0.20.1/24  (02:03:04:05:06:21)

```sh
# Create Topology
$ sudo topo.sh -c

# Destroy Topology
$ sudo topo.sh -d
```

## Run Test

```
$ ./run-ptf-test.sh


sudo ip link add name veth100 type veth peer name veth101
sudo ip link set veth100 up
sudo ip link set veth101 up
```