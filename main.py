"""
main.py: file to run code from
"""

# import src.data_loading.chernobyl as cher
import src.preprocessing.rast_to_poly as rtp

rtp.test_rast()

rtp.trial_esa_cci()

# bio_data = cher.get_bio()
# print(bio_data)
# cher.plot_together()
# cher.get_geoj()

