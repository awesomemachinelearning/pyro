import pyro


def get_parents(node, trace):
    """
    Get the parents of a node in a trace
    TODO docs
    """
    raise NotImplementedError("not implemented yet")


class Trace(dict):
    """
    Execution trace data structure
    """
    def add_sample(self, name, sample, fn, *args, **kwargs):
        """
        Sample site
        """
        assert name not in self, "sample {} already in trace".format(name)
        site = {}
        site["type"] = "sample"
        site["value"] = sample
        site["fn"] = fn
        site["args"] = (args, kwargs)
        if 'baseline_input' in kwargs:
            site["baseline_input"] = kwargs['baseline_input']
        self[name] = site
        return self

    def add_observe(self, name, val, fn, obs, *args, **kwargs):
        """
        Observe site
        """
        assert name not in self, "observe {} already in trace".format(name)
        site = {}
        site["type"] = "observe"
        site["value"] = val
        site["fn"] = fn
        site["obs"] = obs
        site["args"] = (args, kwargs)
        self[name] = site
        return self

    def add_map_data(self, name, data, fn):
        """
        map_data site
        """
        assert name not in self, "map_data {} already in trace".format(name)
        site = {}
        site["type"] = "map_data"
        # XXX
        self[name] = site
        return self

    def add_param(self, name, val, *args, **kwargs):
        """
        param site
        """
        site = {}
        site["type"] = "param"
        site["value"] = val
        site["args"] = (args, kwargs)
        self[name] = site
        return self

    def add_args(self, args_and_kwargs):
        """
        input arguments site
        """
        name = "_INPUT"
        assert name not in self, "_INPUT already in trace"
        site = {}
        site["type"] = "args"
        site["args"] = args_and_kwargs
        self[name] = site
        return self

    def add_return(self, val, *args, **kwargs):
        """
        return value site
        """
        name = "_RETURN"
        assert name not in self, "_RETURN already in trace"
        site = {}
        site["type"] = "return"
        site["value"] = val
        self[name] = site
        return self

    def copy(self):
        """
        Make a copy (for dynamic programming)
        """
        return Trace(self)

    def log_pdf(self):
        """
        Compute the local and overall log-probabilities of the trace
        """
        log_p = 0.0
        for name in self.keys():
            if self[name]["type"] in ("observe", "sample"):
                self[name]["log_pdf"] = self[name]["fn"].log_pdf(
                    self[name]["value"],
                    *self[name]["args"][0],
                    **self[name]["args"][1])
                log_p += self[name]["log_pdf"]
        return log_p

    def batch_log_pdf(self):
        """
        Compute the local and overall log-probabilities of the trace
        """
        log_p = 0.0
        for name in self.keys():
            if self[name]["type"] in ("observe", "sample"):
                self[name]["batch_log_pdf"] = self[name]["fn"].batch_log_pdf(
                    self[name]["value"],
                    *self[name]["args"][0],
                    **self[name]["args"][1])
                log_p += self[name]["batch_log_pdf"]
        return log_p
