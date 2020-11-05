from pyo import *

class GetSig(PyoObject):
    """
    Signal Getter.

    Trying to get a signal value for use elsewhere in python

    :Parent: :py:class:`PyoObject`

    :Args:

        input : PyoObject
            Input signal to process.

    >>> s = Server().boot()
    >>> s.start()
    >>> src = SfPlayer(SNDS_PATH+"/transparent.aif", loop=True, mul=.3)
    >>> lfo = Sine(.25, phase=[0,.5], mul=.5, add=.5)
    >>> ring = RingMod(src, freq=[800,1000], mul=lfo).out()

    """
    def __init__(self, input, mul=1, add=0):
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._in_fader = InputFader(input)
        in_fader,mul,add,lmax = convertArgsToLists(self._in_fader,mul,add)
        self._base_objs = self._ring.getBaseObjects()

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.

        :Args:

            x : PyoObject
                New signal to process.
            fadetime : float, optional
                Crossfade time between old and new input. Defaults to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)

    def play(self, dur=0, delay=0):
        return PyoObject.play(self, dur, delay)

    def stop(self):
        return PyoObject.stop(self)

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        return PyoObject.out(self, chnl, inc, dur, delay)

    @property # getter
    def input(self):
        """PyoObject. Input signal to process."""
        return self._input
    @input.setter # setter
    def input(self, x):
        self.setInput(x)

# Run the script to test the RingMod object.
if __name__ == "__main__":
    s = Server().boot()
    src = SfPlayer(SNDS_PATH+"/transparent.aif", loop=True, mul=.3)
    lfo = Sine(.25, phase=[0,.5], mul=.5, add=.5)
    ring = RingMod(src, freq=[800,1000], mul=lfo).out()
    s.gui(locals())