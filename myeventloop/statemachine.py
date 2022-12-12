from . import Timeout, Log

class StateMachine:
    def __init__(self, name):
        self.name = name
        self.states = {"initial": None}
        self.transitions = {}
        self.state = "initial"
        self.observers = {}
        self.destroyed = False

    def destroy(self):
        if self.destroyed:
            raise Exception("SM destroyed twice")
        self.log_debug2("sm destroyed")
        self.cancel_state_tasks()

    def cancel_state_tasks(self):
        Timeout.cancel_and_inval_by_owner(self)

    def add_state(self, name, callback):
        self.states[name] = callback

    def add_transition(self, from_name, to_name):
        if from_name not in self.transitions:
            self.transitions[from_name] = {}
        self.transitions[from_name][to_name] = 1

    def timeout(self, label, relative_to, callback):
        """
        Creates a timeout owned by this Handler. Timeouts created this way
        are automatically cancelled and invalidated upon state transition.

        Arguments:
            label: a human-readable label for the Timeout
            relative_to: time in seconds into the future
            callback: the function to be called back after the time
        """
        if self.destroyed:
            raise Exception("called StateMachine.timeout() after destroy()")
        return Timeout(self, label, relative_to, callback)

    def schedule_trans(self, new_state, relative_to):
        def cb(_):
            self._trans(new_state)
        return Timeout(self, self.name + ":to_" + new_state, relative_to, cb)

    def trans_now(self, new_state):
        self.cancel_state_tasks()
        self.schedule_trans(new_state, 0)

    def state_match(self, state):
        return state == self.state or \
                state == "*" or \
                (state[0] == "!" and state[1:] != self.state)

    def run_observers(self):
        for name in list(self.observers.keys()):
            if name in self.observers:
                state, cb = self.observers[name]
                if self.state_match(state):
                    del self.observers[name]
                    cb()

    def observe(self, name, state, cb):
        self.observers[name] = (state, cb)
        def run_observers(_):
            self.run_observers()
        Timeout(self, "new_observe", 0, run_observers)

    def unobserve(self, name):
        if name in self.observers:
            del self.observers[name]

    def _trans(self, to_state):
        if to_state not in self.transitions[self.state]: # pragma: no cover
            Log.debug2("*** Invalid trans %s %s %s" % (self.name, self.state, to_state))
            return False
        self.cancel_state_tasks()
        Log.debug2("%s: %s -> %s" % (self.name, self.state, to_state))
        self.state = to_state
        self.states[self.state]()
        def run_observers(_):
            self.run_observers()
        Timeout(self, "trans_observe", 0, run_observers)
