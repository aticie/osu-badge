from MagicInvestigator import Investigator
from circleguard.loader import Loader
from circleguard.replay import ReplayPath, ReplayMap
from circleguard import Circleguard, utils, Circleguard, Check
from circleguard import ReplayPath
from circleguard.enums import Keys, Mod
from slider import Beatmap, Library
from ossapi import ossapi
import scipy.interpolate as interp
import numpy as np
import os
import scipy
from badgeWidget import VisualizerWindow
from PyQt5.QtWidgets import QApplication

USER = "4504101"
MAP = "2097898"
OSU_API_KEY = ""
USE_REPLAY = False  # if the file should be used instead of downloading the replay
REPLAY_PATH = "./replay/nonexistingfile.osr"
CACHE_DIR = "./cache/"
_api = ossapi(OSU_API_KEY)
_cg = Circleguard(OSU_API_KEY)
_loader = _cg.loader
if not os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)
_library = Library.create_db(CACHE_DIR)


def _get_score_info():
    print("@retrieving score info")
    return _api.get_scores({"b":MAP, "u":USER})[0]

def _get_replay(score_info):
    if USE_REPLAY:
        print("@USE_REPLAY set, using REPLAY_PATH")
        replay = ReplayPath(REPLAY_PATH)
    else:
        print("@USE_REPLAY not set, trying to download replay")
        if score_info["replay_available"] != "0":
            print("@Downloading Replay")
            replay = ReplayMap(user_id=USER,map_id=MAP)
        else:
            print("@No replay available")
            exit(-1)
    replay.load(_loader)
    print("@"+replay.__str__())
    return replay

def _get_graph_data(rp):
    global hit_map
    # inizilaite _cg
    _cg = Circleguard(OSU_API_KEY)

    # get beatmap
    bm = _library.lookup_by_id(MAP, download=True, save=True)

    # generate Investigator class
    investigator = Investigator(rp, bm, -1)

    # get hit_map
    hit_map = investigator.hit_map(0)

    # get diff list
    diffs_old = [i.error for i in hit_map]
    d = [diffs_old[i+1]-diffs_old[i] for i in range(len(diffs_old)-1)]
    list(d)
    diffs = np.array(d)
    arr1_interp = interp.interp1d(np.arange(diffs.size),diffs)
    arr1_compress = arr1_interp(np.linspace(0,diffs.size-1,16))
    # make everything positiv
    offset = min(arr1_compress)*-1
    arr1_compress = [i+offset for i in arr1_compress]
    # make normalize to 0-1
    scale = max(arr1_compress)
    arr1_compress = [i/scale for i in arr1_compress]
    arr1_compress = np.array(arr1_compress)
    _cg.library.close()

    return arr1_compress

def _get_norm_hit_map(rp):
    mods1 = [Mod(mod_val) for mod_val in utils.bits(rp.mods)]
    flip1 = Mod.HardRock in mods1
    # inizilaite _cg
    _cg = Circleguard(OSU_API_KEY)

    # get beatmap
    bm = _library.lookup_by_id(MAP, download=True, save=True)

    # generate Investigator class
    investigator = Investigator(rp, bm, -1)

    # get hit_map
    hit_map = investigator.hit_map(flip1)
    circle_size = (109 - 9 * bm.circle_size)
    new_hitmap = []
    for i in hit_map:
        i.x = i.x/circle_size
        i.y = i.y/circle_size
        new_hitmap.append(i)
    _cg.library.close()    
    return new_hitmap

if __name__ == "__main__":
    score_info = _get_score_info()
    replay = _get_replay(score_info)
    graph = _get_graph_data(replay)
    hit_map  = _get_norm_hit_map(replay)
    app = QApplication([])
    visualizer_window = VisualizerWindow(score_info, graph, hit_map)
    _cg.library.close()
    # remove comment to display after saving
    """visualizer_window.show() 
    app.exec_()"""
