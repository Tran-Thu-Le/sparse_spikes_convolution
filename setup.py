import numpy as np 
from numpy.linalg import norm
import matplotlib.pyplot as plt


def dic(x, t, w):
    """
        x: coordinates
        t: positions
        w: half_width
    """
    diff = x.T.reshape(-1, 2, 1) - t
    dist = norm(diff, axis=1)
    dic_ = np.power(2, -dist**2/w**2)
    norm_ = norm(dic_, axis=0)
    assert norm_.shape[0] == dic_.shape[1]
    return dic_/norm_

def get_raw_input():
    positions = "[[0.1, 0.1], [0.5, 0.7], [0.9, 0.7]]"
    amplitudes = "[1., 2., 0.6]"    
    half_width = "0.1"
    contour_color = "Reds"
    spike_marker = "+"
    color_bar = "on"
    raw_data = {
        'positions': positions,
        'amplitudes': amplitudes,
        'half_width': half_width,
        'contour_color': contour_color,
        'spike_marker': spike_marker,
        'color_bar': color_bar,
    }
    return raw_data

def process_input(raw_data):
    # raw_data = get_raw_input()
    data = raw_data.copy()
    # data["half_width"] = raw_data["half_width"]
    data["positions"] = np.array(eval(raw_data["positions"])).T
    data["amplitudes"] = np.array(eval(raw_data["amplitudes"]))
    return data

def set_up(data):   

    wa, wb = -0.2, 1.2
    wm = 50
    dw = (wb-wa)/wm
    m = wm**2
    w_axis = np.linspace(wa, wb, wm+1) 
    w_axis = w_axis[: -1] + dw/2 
    w_grid = np.meshgrid(w_axis, w_axis) 
    w = np.stack([w_grid[0].reshape(-1), w_grid[1].reshape(-1)], axis = 0) 

    ta, tb = 0., 1.
    tn = 60
    dt = (tb-ta)/tn 
    n = tn**2
    t_axis = np.linspace(ta, tb, tn+1) 
    t_axis = t_axis[: -1] + dt/2 
    t_grid = np.meshgrid(t_axis, t_axis) 
    t = np.stack([t_grid[0].reshape(-1), t_grid[1].reshape(-1)], axis=0) 

    # data = process_input()
    atoms_true = dic(x=w, t=data["positions"], w=data["half_width"])

    # dinf y 
    obs = atoms_true @ data["amplitudes"].reshape(-1, 1)

    my_setup = {
        "xa": wa,
        "xb": wb,
        "xm": wm,
        "m": m,
        "dx": dw,
        "x_axis": w_axis,
        "x_grid": w_grid,
        "x": w,
        
        "ta": ta,
        "tb": tb,
        "tn": tn,
        "n": n,
        "dt": dt,
        "t_axis": t_axis,
        "t_grid": t_grid,
        "t": t,

        "obs": obs
    }

    return my_setup 

def plot(raw_data, data, setup):
    # raw_data = get_raw_input()
    # data = process_input(raw_data)
    # setup = set_up(data)
    obs = setup["obs"]
    x_grid = setup["x_grid"]
    xm = setup["xm"]
    pos = data["positions"]
    p0, p1 = pos
    amp = data["amplitudes"]
    color_bar = data["color_bar"]
    marker = data["spike_marker"]
    cmap = data["contour_color"]

    f, ax = plt.subplots(figsize=(15, 9))
    cb = ax.contourf(x_grid[0], x_grid[1], obs.reshape(xm, xm),
                cmap=cmap, levels=100, vmin=0., vmax=obs.max()) 
    ax.scatter(p0, p1, marker=marker, s=amp*600, c="white", edgecolors='black')   
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    if color_bar == "on":
        f.colorbar(cb, ax=ax)

    return f 


if __name__=="__main__":
    raw_data = get_raw_input()
    data = process_input(raw_data)
    setup = set_up(data)
    fig = plot(raw_data, data, setup)
    plt.show()

