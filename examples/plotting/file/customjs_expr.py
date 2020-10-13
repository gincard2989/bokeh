import numpy as np

from bokeh.core.properties import Float, expr
from bokeh.io import save
from bokeh.model import Model
from bokeh.models import ColumnDataSource, CustomJSExpr
from bokeh.plotting import figure


class Params(Model):
    __data_model__ = True

    amp = Float(default=0.1, help="Amplitude")
    freq = Float(default=0.1, help="Frequency")
    phase = Float(default=0, help="Phase")
    offset = Float(default=-5, help="Offset")

params = Params(amp=2, freq=3, phase=0.4, offset=1)

x = np.linspace(0, 10, 100)
y = CustomJSExpr(args=dict(params=params), code="""
    const A = params.amp
    const k = params.freq
    const phi = params.phase
    const B = params.offset
    const {x} = this.data
    return x.map((xi) => A*Math.sin(k*xi + phi) + B)
    /* Alternatively:
    for (const xi of x) {
      yield A*Math.sin(k*xi + phi) + B
    }
    */
""")

plot = figure(tags=[params], y_range=(-5, 5), title="Data models with custom JS expressions")
plot.line(x, y=expr(y), line_width=3, line_alpha=0.6)

# TODO: callback = emit exprchange
#params.js_on_change("amp", callback)
#params.js_on_change("freq", callback)
#params.js_on_change("phase", callback)
#params.js_on_change("offset", callback)

save(plot)