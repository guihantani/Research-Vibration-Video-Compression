from video_processing import Video
from video_processing import Video_Magnification
from video_processing import h5py_tools
import numpy as np


video_path = 'video_samples/beam.avi'

beam_number_components = 8
structure_number_components = 12
three_beams_number_components = 20

number_components = beam_number_components
components_order = np.arange(number_components)
sources_order = np.arange(number_components)

beam_coordinates_order = np.array([0, 1, 2, 3, 6, 7])
structure_coordinates_order = np.array([14, 15, 2, 3, 5, 6])
three_beams_coordinates_order = np.array([4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
waves_coordinates_order = np.array([0, 1, 8, 9, 10, 11])
all_coordinates = np.arange(number_components)

modal_coordinates_order = beam_coordinates_order

beam_factors = np.array([30, 15, 5])
structure_factors = np.array([5, 15, 30])
three_beams_factors = np.array([15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15])
all_factors = np.ones(number_components) * 30

factors = beam_factors

# set the video object
video = Video(video_path)

if video_path == 'video_samples/three_beams.avi':
    video.crop_video(3016)
elif video_path == 'video_samples/waves.avi':
    video.crop_video(120)

# Start video magnification
magnification = Video_Magnification(video)
magnification.create_video_from_frames("frames_gray", frames=video.gray_frames)


# Create time series
time_serie = magnification.create_time_series()

# Remove background
magnification.remove_background()

# Hibert Transform
real_time_serie, imag_time_serie = magnification.apply_hilbert_transform()

# dimension reduction in the real and imaginary time series
eigen_vectors, eigen_values, components = magnification.dimension_reduction()

# vizualize principal components
magnification.visualize_components_or_sources('components', components_order)

# blind source separation
mixture_matrix, sources = magnification.extract_sources(number_components)

# visualize sources
magnification.visualize_components_or_sources('sources', sources_order)

# create mode shapes and modal coordinates
mode_shapes, modal_coordinates = magnification.create_mode_shapes_and_modal_coordinates(number_components,
                                                                                              modal_coordinates_order)
                                                                                              
# visualize modal coordinates and mode shapes
magnification.visualize_mode_shapes_and_modal_coordinates(modal_coordinates_order)

# visualize only modal coordinates
magnification.visualize_components_or_sources('modal coordinates', np.arange(len(modal_coordinates_order)))

# video reconstruction
number_of_modes = modal_coordinates_order.size//2
mother_matrix = magnification.video_reconstruction(number_of_modes, factors)

for result in range(number_of_modes + 1):
# for result in range(1):
    magnification.create_video_from_frames("mode%d" % result, frames=mother_matrix[result])

# saving matrices
mode_shapes = magnification.mode_shapes.astype("int16")
h5py_tools.save_matrix(mode_shapes.astype("float16"), "mode_shapes")
h5py_tools.save_matrix(magnification.modal_coordinates.astype("float16"), "modal_coordinates")
background = np.copy(magnification.time_serie_mean.astype("uint8"))
h5py_tools.save_matrix(background, "background")

# reading matrices
# magnification.mode_shapes = h5py_tools.read_matrix("mode_shapes")
# magnification.modal_coordinates = h5py_tools.read_matrix("modal_coordinates")
# magnification.time_serie_mean = h5py_tools.read_matrix("background")
