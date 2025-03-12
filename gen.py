import numpy as np
# from order import Order
# from bed import Bed

class Gen():
    def __init__(self,
            orders: list[int], beds: list[int], bed_nbr_slots_x: int,
            bed_nbr_slots_y: int, nbr_time_slots: int):
        nbr_pontons = 0
        for order in orders:
            # nbr_pontons_of_order = len(order.pontons) # np.shape(order.pontons)[0]
            nbr_pontons_of_order = order # this is temporary until intergration with Jesper
            nbr_pontons += nbr_pontons_of_order
        self.nbr_pontons = nbr_pontons
        nbr_beds = len(beds)
        self.nbr_bins_beds = np.shape(self._nbr2Bins(nbr_beds))[0]
        self.bed_nbr_slots_x = np.shape(self._nbr2Bins(bed_nbr_slots_x))[0]
        self.bed_nbr_slots_y = np.shape(self._nbr2Bins(bed_nbr_slots_y))[0]
        self.nbr_bins_time = np.shape(self._nbr2Bins(nbr_time_slots))[0]
        self.bins_sizes = [
            self.nbr_bins_beds,
            self.bed_nbr_slots_x,
            self.bed_nbr_slots_y,
            self.nbr_bins_time
        ]
        self.total_bins_per_ponton = sum(self.bins_sizes)
        self.gen = np.zeros([nbr_pontons*self.total_bins_per_ponton,],dtype=int)

    def _nbr2Bins(self, nbr):
        bins = np.array([int(bit) for bit in bin(nbr)[2:]])
        return bins
    
    def _bins2Nbr(self, bins):
        powers = 2 ** np.arange(len(bins))[::-1]
        nbr = np.dot(bins, powers)
        return nbr
    
    def randomize_gen(self):
        for iGenome, _ in enumerate(self.gen):
            r = np.random.uniform(0, 1)
            self.gen[iGenome] = 1 if r < 0.5 else 0
        return self
    
    def encode_ponton(self, ponton_index, bed_id, bed_x, bed_y, start_time):
        def left_pad_bins(bins,pad_to):
            pad_length = pad_to - np.shape(bins)[0]
            padded_bins = np.pad(bins,(pad_length,0),mode="constant",constant_values=0)
            return padded_bins
        ponton_first_index = self.total_bins_per_ponton*ponton_index
        ponton_last_index = self.total_bins_per_ponton*(ponton_index + 1)
        ponton_bin = self.gen[ponton_first_index:ponton_last_index]
        toEncode = [bed_id, bed_x, bed_y, start_time]
        current_index = 0
        for iEncode, encode in enumerate(toEncode):
            bin_size = self.bins_sizes[iEncode]
            bins = left_pad_bins(self._nbr2Bins(encode),bin_size)
            ponton_bin[current_index:current_index + bin_size] = bins
            current_index += bin_size
        return self
    
    def decode_ponton(self,ponton_index):
        ponton_first_index = self.total_bins_per_ponton*ponton_index
        ponton_last_index = self.total_bins_per_ponton*(ponton_index + 1)
        ponton_bin = self.gen[ponton_first_index:ponton_last_index]
        current_index = 0
        bed_id_bins = ponton_bin[current_index:current_index+self.nbr_bins_beds]
        current_index += self.nbr_bins_beds
        bed_x_bins = ponton_bin[current_index:current_index+self.bed_nbr_slots_x]
        current_index += self.bed_nbr_slots_x
        bed_y_bins = ponton_bin[current_index:current_index+self.bed_nbr_slots_y]
        current_index += self.bed_nbr_slots_y
        start_time_bins = ponton_bin[current_index:current_index+self.nbr_bins_time]
        bed_id = self._bins2Nbr(bed_id_bins)
        bed_x = self._bins2Nbr(bed_x_bins)
        bed_y = self._bins2Nbr(bed_y_bins)
        start_time = self._bins2Nbr(start_time_bins)
        return (bed_id,bed_x,bed_y,start_time)

    def fittnes_score(self):
        fittnes_score = 0
        for _ in self.gen:
            fittnes_score += np.random.uniform(0, 1)
        return fittnes_score