"""KismetDB logs abstraction"""

from .base_interface import BaseInterface


class KismetDB(BaseInterface):
    """KismetDB logs abstraction"""
    
    kwargs_defaults = {"title": "packets"}
    url_template = "logging/kismetdb/pcap/{title}.pcapng"
    
    def packets(self, filter=None, **kwargs):
        """Yield packets, one at a time.
        
        If callback is set, nothing will be returned.
        
        Keyword args:
            title (str): File download title, does not impact pcap file generation.
        
        Yield:
            bytes: A pcapng stream will be generated of packets, if any, matching the filter options.
        """
        cmd = {}
        if filter:
            cmd["filter"] = filter
        query_args = self.kwargs_defaults.copy()
        query_args.update(kwargs)
        url = self.url_template.format(**query_args)
        return self.interact("POST", url, payload=cmd, return_bytes=True)
    
    def drop_packets(self, drop_before):
        """Dropping packets
        
        On very long-running Kismet processes, you may wish to purge old packets. 
        These packets will be removed from the kismetdb log.
        
        Args:
            drop_before (int): A unix second timestamp value, packets older than drop_before will be deleted.
        
        Return:
            bool: True for success, False for failed request
        """
        cmd = {"drop_before": drop_before}
        url = "logging/kismetdb/pcap/drop.cmd"
        return self.interact("POST", url, payload=cmd, only_status=True)