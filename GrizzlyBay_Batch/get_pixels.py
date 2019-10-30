# Script to read in Envi file, get pixels and batch Script
import json
import scipy as s
import numpy as np

# Load Wavelengths
wavelengths = np.loadtxt('C:\\Users\\MonicaVermillion\\Documents\\JPL\\prism\\GrizzlyBay_Batch\\data\\wavelength.txt')
wave = wavelengths[:,1]


# Load in the lines and samples to grab from the image
overlap = np.loadtxt('lines-samples-950.txt')
lines = overlap[:,0] # Rows
samples = overlap[:,1] # Columns

# Load the data and convert to Band-In-Pixel interleave
filename = 'C:\\Users\\MonicaVermillion\\Documents\\JPL\\prism\\prm\\prm20140428t230950_rdn_v1c\\prm20140428t230950_rdn_v1c_img'
rows, bands, cols = 4944,246,721
mm = s.memmap(filename, dtype=s.float32, mode='r',shape=(rows,bands,cols))

d = s.asarray(mm,dtype = s.float32).copy() # Takes a little while to run


# Grab the pixels that overlap:
#for j,k in enumerate(lines)
    #col = samples[j]
    #pixel = d[samp,k,4:-1]

t_line = int(lines[0]) # Test line
t_sample = int(samples[0]) # Test sample
pixel = d[t_line,4:,t_sample]
#plt.plot(pixel)

rad_stack = np.column_stack((wave,pixel))
#for h in range(3):
base_name = 'prm20140428t230950_'+str(t_line)+'_'+str(t_sample)
radiance_input = 'remote/'+base_name+'_rad.txt'
np.savetxt(radiance_input,rad_stack, delimiter=" ") #format is a string?


config_isofit = {}
config_isofit ={
    "ISOFIT_base": "../../..",

      "input": {
        "measured_radiance_file": "../remote/prm20140428t230950.txt"
      },

      "output": {
        "estimated_reflectance_file": "../output/prm20140428t2309505_rfl.txt",
        "modeled_radiance_file":      "../output/prm20140428t230950_mdl.txt",
        "state_file":                 "../output/prm20140428t230950_state.txt",
        "posterior_uncertainty_file": "../output/prm20140428t230950_post.txt",
        "data_dump_file":             "../output/prm20140428t230950_data.mat"

      },

      "forward_model":{

        "instrument": {
          "wavelength_file":    "../data/wavelengths.txt",
          "SNR": 500,
          "integrations":25
        },

        "glint_surface": {
          "surface_file": "../data/prm20140428_surface_coastal_model.mat"
        },

        "sixs_radiative_transfer": {
          "irradiance_file":         "../data/prism_optimized_irr.dat",
          "earth_sun_distance_file": "../../../data/earth_sun_distance.txt",
          "wavelength_file":         "../data/wavelengths.txt",
          "sixs_installation":       "",
          "solzen": 44.50,
          "elev":  0.0,
          "alt": 3.041,
          "solaz": 249.37,
          "viewzen": 4.90,
          "viewaz": 319.61,
          "month": 4,
          "day": 28,
          "lut_path":"../lut/",
          "domain": {"start": 350, "end": 2520, "step": 0.1},
          "statevector": {
            "H2OSTR": {
              "bounds": [0.5, 1.0],
              "scale": 0.01,
              "prior_sigma": 100.0,
              "prior_mean": 1.0,
              "init": 0.75
            },
            "AOT550": {
              "bounds": [0.0, 0.1],
              "scale": 0.1,
              "prior_mean": 0.05,
              "prior_sigma": 100.0,
              "init": 0.04
            }
          },
          "lut_grid": {
            "H2OSTR": [0.5,0.7,1.0],
            "AOT550": [0.0,0.05,0.1]
          },
          "unknowns": {
            "H2O_ABSCO": 0.01
          }
        }
      },

      "inversion": {
        "windows": [[400.0,1000.0]]
      }
    }




config_isofit["input"]["measured_radiance_file"] =         '../'+radiance_input
config_isofit["output"]["estimated_reflectance_file"] =   '../output/reflectance/'+base_name+'_rfl.txt'
config_isofit["output"]["modeled_radiance_file"] =        '../output/mod_radiance/'+base_name+'_mdl.txt'
config_isofit["output"]["state_file"] =                   '../output/state/'+base_name+'_state.txt'
config_isofit["output"]["posterior_uncertainty_file"] =   '../output/posterior_uncertainty/'+base_name+'_post.txt'
config_isofit["output"]["data_dump_file"] =               '../output/datadump/'+base_name+'_data.txt'

# Write the config file for that pixel
config_name = 'configs/'+base_name+'.json'
with open(config_name, "w") as write_file:
    json.dump(config_isofit,write_file,indent=4)

# Write the bash file to run the pixel
bash_name = 'run_'+base_name+'.sh' # name of bash script file
isofit_dir = 'export isofit="../../../isofit/isofit.py"' # place isofit dir
bash_add = 'python ${isofit} --level DEBUG '+config_name #bash script input


with open (bash_name, 'a') as rsh:
    rsh.write(isofit_dir+'\n')
    rsh.write(bash_add+'\n')
    rsh.close()
