import unittest

from migen import *

from artiq.gateware.drtio.rt_packets import *


class PacketInterface:
    def __init__(self, direction, frame, data):
        if direction == "m2s":
            self.plm = get_m2s_layouts(len(data))
        elif direction == "s2m":
            self.plm = get_s2m_layouts(len(data))
        else:
            raise ValueError
        self.frame = frame
        self.data = data

    def send(self, ty, **kwargs):
        idx = 8
        value = self.plm.types[ty]
        for field_name, field_size in self.plm.layouts[ty][1:]:
            try:
                fvalue = kwargs[field_name]
                del kwargs[field_name]
            except KeyError:
                fvalue = 0
            value = value | (fvalue << idx)
            idx += field_size
        if kwargs:
            raise ValueError

        ws = len(self.data)
        yield self.frame.eq(1)
        for i in range(idx//ws):
            yield self.data.eq(value)
            value >>= ws
            yield
        yield self.frame.eq(0)
        yield

    @passive
    def receive(self, callback):
        previous_frame = 0
        frame_words = []
        while True:
            frame = yield self.frame
            if frame:
                frame_words.append((yield self.data))
            if previous_frame and not frame:
                packet_type = self.plm.type_names[frame_words[0] & 0xff]
                packet_nwords = layout_len(self.plm.layouts[packet_type]) \
                                //len(self.data)
                packet, trailer = frame_words[:packet_nwords], \
                                  frame_words[packet_nwords:]

                n = 0
                packet_int = 0
                for w in packet:
                    packet_int |= (w << n)
                    n += len(self.data)

                field_dict = dict()
                idx = 0
                for field_name, field_size in self.plm.layouts[packet_type]:
                    v = (packet_int >> idx) & (2**field_size - 1)
                    field_dict[field_name] = v
                    idx += field_size

                callback(packet_type, field_dict, trailer)

                frame_words = []
            previous_frame = frame
            yield


class TestSatellite(unittest.TestCase):
    def test_echo(self):
        for nwords in range(1, 8):
            dut = RTPacketSatellite(nwords)
            pt = PacketInterface("m2s", dut.rx_rt_frame, dut.rx_rt_data)
            pr = PacketInterface("s2m", dut.tx_rt_frame, dut.tx_rt_data)
            completed = False
            def send():
                yield from pt.send("echo_request")
                while not completed:
                    yield
            def receive(packet_type, field_dict, trailer):
                nonlocal completed
                self.assertEqual(packet_type, "echo_reply")
                self.assertEqual(trailer, [])
                completed = True
            run_simulation(dut, [send(), pr.receive(receive)])
