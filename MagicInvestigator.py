from circleguard.investigator import Investigator as _cg_inv, Hit


class Investigator(_cg_inv):  # add hit_map func back
    def hit_map(self, flip):	
        hitobjs = self._parse_beatmap(self.beatmap)
        keypresses = self._parse_keys(self.data)
        filtered_array = self._filter_hits(hitobjs,keypresses)
        array = []	
        for hit, press in filtered_array:	
            array.append(stupid_hr_hit(hit,press,flip))	
        return array


class stupid_hr_hit(Hit):
    def __init__(self, hit, hitobj, flip):
        self.x = hit[1]-hitobj[1]
        self.y = hit[2]-hitobj[2] if not flip else hit[2]-(384-hitobj[2])
        self.error = hit[0]-hitobj[0]