Grizzly Bay Batch
-----------------------------------------------------------------------
/bash_scripts

  -prm20140428t230950_line_sample.sh

  Shell scripts to run the surface model and then run all of the
  python files for ISOFIT
------------------------------------------------------------------------
/configs

  -surface_model_grizzly.json
  -prm20140428t230950_line_sample.json

  json config files that change radiance and then change
  output, this contians the surface config file to be called
  first and then all of the configs for the following radiance spectra
-----------------------------------------------------------------------
/data

  -wavelengths.txt

  Format: 

-----------------------------------------------------------------------
/lut

  6SV Look up tables for the scene
-----------------------------------------------------------------------
/output
  /datadump


  /mod_radiance # modeled radiance file

      -prm20140428t230950_line_sample_mod_rad.txt

  /reflectance # ouputed reflectance

      -prm20140428t230950_line_sample_ref.txt
  /state

  /posterior_uncertainty

-----------------------------------------------------------------------
/remote

  prm20140428t230950_line_sample.txt

  PRISM radiance files, clipped from .36 microns, wavelenth then
  radiance
