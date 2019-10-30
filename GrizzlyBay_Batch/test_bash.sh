# David R Thompson
export isofit="../../isofit/isofit.py"
export surfmodel="../../utils/surfmodel.py"

# Build the surface model
python ${isofit} --level DEBUG configs/prm20140428t230950_3403_624.json
