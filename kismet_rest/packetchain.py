"""Packet processing endpoint."""
import datetime

from .base_interface import BaseInterface
from .exceptions import KismetServiceError


class Packetchain(BaseInterface):
    """Wrap all interaction with /packetchain/ endpoint."""

    def _order_rrd(data, rrdtype, timestamp):
        """Re-order a RRD ring

        Args: 
            data (array) RRD data ring 

            rrdtype (string) rrd type

            timestamp (number) serialization timestamp 
        """

        ts_slot = 0

        if rrdtype == "minute":
            ts_slot = (timestamp % len(data))
        elif rrdtype == "hour":
            ts_slot = int(timestamp / 60) % len(data)
        elif rrdtype == "day": 
            ts_slot = int(timestamp / 3600) % len(data)
        else:
            msg = "Unknown rrd type {}".format(rrdtype)
            raise KismetServiceError(msg, -1)

        return data[ts_slot + 1:] + data[:ts_slot + 1]

    def get_packet_stats(self, category, timeline):
        """Get the packet statistics for a given category and timeline. 

        Args:
            category (str or array): Category to get packets from; 
                processed
                dropped 
                queued
                peak 
                dupe
                packets 

            timeline (str): Timeline to fetch packets from;
                minute
                hour
                day

        Return: 
            Array of RRD data or array of arrays of RRD data if multiple 
            categories are requested
        """

        categories = {
                "processed": "kismet.packetchain.processed_packets_rrd",
                "dropped": "kismet.packetchain.dropped_packets_rrd",
                "queued": "kismet.packetchain.queued_packets_rrd",
                "peak": "kismet.packetchain.peak_packets_rrd",
                "dupe": "kismet.packetchain.dupe_packets_rrd",
                "packets": "kismet.packetchain.packets_rrd",
                }

        times = {
                "minute": "kismet.common.rrd.minute_vec",
                "hour": "kismet.common.rrd.hour_vec",
                "day": "kismet.common.rrd.day_vec",
                }

        if isinstance(category, list):
            for c in category:
                if not c in categories:
                    msg = "Invalid category: {}".format(c)
                    raise KismetServiceError(msg, -1)
        else:
            if not category in categories:
                msg = "Invalid category: {}".format(category)
                raise KismetServiceError(msg, -1)

        if not timeline in times:
            msg = "Invalid timeline: {}".format(timeline)
            raise KismetServiceError(msg, -1)

        fields = []

        if isinstance(category, list):
            for c in category:
                f1 = "{}/kismet.common.rrd.serial_time".format(categories[c])
                f2 = "{}_time".format(c)
                fields.append([f1, f2])

                f1 = "{}/{}".format(categories[c], times[timeline])
                f2 = "{}_data".format(c)
                fields.append([f1, f2])
        else:
            f1 = "{}/kismet.common.rrd.serial_time".format(categories[category])
            f2 = "{}_time".format(category)
            fields.append([f1, f2])

            f1 = "{}/{}".format(categories[category], times[timeline])
            f2 = "{}_data".format(category)
            fields.append([f1, f2])

        payload = {"fields": fields}
        data = self.interact("POST", "packetchain/packet_stats.json", payload=payload)

        if isinstance(category, list):
            ret = []

            for c in category:
                f1 = "{}_data".format(c)
                f2 = "{}_time".format(c)

                if not f1 in data or not f2 in data: 
                    msg = "Missing response {} / {} in data".format(f1, f2)
                    raise KismetServiceError(msg, -1)

                ret.append(Packetchain._order_rrd(data[f1], timeline, data[f2]))

            return ret
        else:
            f1 = "{}_data".format(category)
            f2 = "{}_time".format(category)

            if not f1 in data or not f2 in data: 
                msg = "Missing response {} / {} in data".format(f1, f2)
                raise KismetServiceError(msg, -1)

            return Packetchain._order_rrd(data[f1], timeline, data[f2])


