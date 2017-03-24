import sys
import os
from subprocess import Popen, PIPE
from cffi import FFI


def _get_env(v):
    _v = os.getenv(v)
    if _v is None:
        sys.stderr.write('Error: Environment variable {0} is undefined\n'.format(v))
        sys.exit(1)
    return _v


def _get_library_suffix():
    if sys.platform == "darwin":
        return 'dylib'
    else:
        return 'so'


def _get_lib_handle(definitions, header, library, build_dir, include_dir):
    ffi = FFI()
    interface = Popen(['cc', '-E'] + definitions + [os.path.join(include_dir, header)],
                      stdout=PIPE).communicate()[0].decode("utf-8")
    ffi.cdef(interface)

    suffix = _get_library_suffix()
    lib = ffi.dlopen(os.path.join(build_dir, 'lib', 'lib{0}.{1}'.format(library, suffix)))
    return lib


_build_dir = _get_env('FLANDERS_BUILD_DIR')
_include_dir = os.path.dirname(os.path.realpath(__file__))

_lib = _get_lib_handle(
    ['-DCPP_INTERFACE_API=', '-DCPP_INTERFACE_NOINCLUDE'],
    'flanders.h',
    'flanders',
    _build_dir,
    _include_dir
)


# outward facing API

def new_context(num_points,
                x_coordinates,
                y_coordinates):

    # cast a pointer which points to the numpy array data
    # we work with numpy because tree initialization with normal lists segfault
    # for lists longer than ca. 0.5 million points
    ffi = FFI()
    x_coordinates_p = ffi.cast("double *", x_coordinates.ctypes.data)
    y_coordinates_p = ffi.cast("double *", y_coordinates.ctypes.data)

    return _lib.new_context(num_points,
                            x_coordinates_p,
                            y_coordinates_p)


free_context = _lib.free_context
find_neighbor = _lib.find_neighbor


def find_neighbor_naive(ref_index,
                        num_points,
                        x_coordinates,
                        y_coordinates,
                        use_angles,
                        view_vector,
                        view_angle_deg):

    # cast a pointer which points to the numpy array data
    # we work with numpy because tree initialization with normal lists segfault
    # for lists longer than ca. 0.5 million points
    ffi = FFI()
    x_coordinates_p = ffi.cast("double *", x_coordinates.ctypes.data)
    y_coordinates_p = ffi.cast("double *", y_coordinates.ctypes.data)

    return _lib.find_neighbor_naive(ref_index,
                                    num_points,
                                    x_coordinates_p,
                                    y_coordinates_p,
                                    use_angles,
                                    view_vector,
                                    view_angle_deg)
