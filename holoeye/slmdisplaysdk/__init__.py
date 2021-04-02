# -*- coding: utf-8 -*-

#--------------------------------------------------------------------#
#                                                                    #
# Copyright (C) 2018 HOLOEYE Photonics AG. All rights reserved.      #
# Contact: https://holoeye.com/contact/                              #
#                                                                    #
# This file is part of HOLOEYE SLM Display SDK.                      #
#                                                                    #
# You may use this file under the terms and conditions of the        #
# "HOLOEYE SLM Display SDK Standard License v1.0" license agreement. #
#                                                                    #
#--------------------------------------------------------------------#


import ctypes
import os
import sys

## \cond INTERNALDOC
## Stores if the current Python version is 3 or higher
isPython3 = sys.version_info[0] == 3
## \endcond

## Stores if NumPy could be found.
# \ingroup SLMDisplayPython
supportNumPy = True

try:
    import numpy
except:
    supportNumPy = False

## Creates a field for a given type description for either numpy or ctypes.
# \ingroup SLMDisplayPython
# \param width The width of the generated array. If \p width or \p height is zero, the slm size will be used.
# \param height The height of the generated array. If \p width or \p height is zero, the slm size will be used.
# \param elementSizeInBytes The size of each element in bytes, for example 4 for an integer.
# \param elementIsReal Defines if the created array will be one of integers or real numbers.
# \param useNumPy When true, a numpy array will be created when it is supported. Otherwise a ctypes array will be created.
# \return A 2d array of the given type based on numpy or ctypes.
def createFieldByType(width, height, elementSizeInBytes, elementIsReal, useNumPy):

    width = int(width)
    height = int(height)

    assert width > 0 and height > 0
    assert elementSizeInBytes > 0

    if useNumPy:
        assert supportNumPy, "NumPy could not be found"

        elementType = None

        if elementIsReal:
            if elementSizeInBytes == 4:
                elementType = numpy.single
            elif elementSizeInBytes == 8:
                elementType = numpy.double
        else:
            if elementSizeInBytes == 1:
                elementType = numpy.ubyte
            elif elementSizeInBytes == 4:
                elementType = numpy.uintc

        assert elementType is not None, "The given format - size:" + str(elementSizeInBytes) + "  real:" + str(elementIsReal) + " - is not supported."

        return numpy.empty((height, width), elementType)

    else:
        elementType = None

        if elementIsReal:
            if elementSizeInBytes == 4:
                elementType = ctypes.c_float
            elif elementSizeInBytes == 8:
                elementType = ctypes.c_double
        else:
            if elementSizeInBytes == 1:
                elementType = ctypes.c_ubyte
            elif elementSizeInBytes == 4:
                elementType = ctypes.c_uint

        assert elementType is not None, "The given format - size:" + str(elementSizeInBytes) + "  real:" + str(elementIsReal) + " - is not supported."

        return ((elementType * width) * height)()

## Creates an unsigned byte array for either numpy or ctypes
# \ingroup SLMDisplayPython
# \param width The width of the generated array. If \p width or \p height is zero, the slm size will be used.
# \param height The height of the generated array. If \p width or \p height is zero, the slm size will be used.
# \param useNumPy When true, a numpy array will be created when it is supported. Otherwise a ctypes array will be created.
# \return A 2d array of unsigned bytes based on numpy or ctypes.
def createFieldUChar(width = 0, height = 0, useNumPy = True):
    if width <= 0 or height <= 0:
        heg = SLMDisplay.Instance
        assert heg is not None, "No SLMDisplay object was created"

        width = heg.width_px
        height = heg.height_px

    return createFieldByType(width, height, 1, False, useNumPy and supportNumPy)

## Creates an array of single real values for either numpy or ctypes.
# \ingroup SLMDisplayPython
# \param width The width of the generated array. If \p width or \p height is zero, the slm size will be used.
# \param height The height of the generated array. If \p width or \p height is zero, the slm size will be used.
# \param useNumPy When true, a numpy array will be created when it is supported. Otherwise a ctypes array will be created.
# \return A 2d array of floats based on numpy or ctypes.
def createFieldSingle(width = 0, height = 0, useNumPy = True):
    if width <= 0 or height <= 0:
        heg = SLMDisplay.Instance
        assert heg is not None, "No SLMDisplay object was created"

        width = heg.width_px
        height = heg.height_px

    return createFieldByType(width, height, 4, True, useNumPy and supportNumPy)

## Creates an array of double real values for either numpy or ctypes.
# \ingroup SLMDisplayPython
# \param width The width of the generated array. If \p width or \p height is zero, the slm size will be used.
# \param height The height of the generated array. If \p width or \p height is zero, the slm size will be used.
# \param useNumPy When true, a numpy array will be created when it is supported. Otherwise a ctypes array will be created.
# \return A 2d array of doubles based on numpy or ctypes.
def createFieldDouble(width = 0, height = 0, useNumPy = True):
    if width <= 0 or height <= 0:
        heg = SLMDisplay.Instance
        assert heg is not None, "No SLMDisplay object was created"

        width = heg.width_px
        height = heg.height_px

    return createFieldByType(width, height, 8, True, useNumPy and supportNumPy)

## Returns the width of the given field.
# \ingroup SLMDisplayPython
# \param field The field whose width we want.
# \return Zero when there was an error. Otherwise a number greater than zero.
def width(field):
    if supportNumPy and isinstance(field, numpy.ndarray):
        assert field.size > 0, "The given array has no size"

    else:
        assert isinstance(field, ctypes.Array), "The provided data must be a ctypes or numpy array"
        assert len(field) > 0, "The given array has no size"

    return len(field[0])

## Returns the height of the given field.
# \ingroup SLMDisplayPython
# \param field The field whose height we want.
# \return Zero when there was an error. Otherwise a number greater than zero.
def height(field):
    if supportNumPy and isinstance(field, numpy.ndarray):
        assert field.size > 0, "The given array has no size"

    else:
        assert isinstance(field, ctypes.Array), "The provided data must be a ctypes or numpy array"
        assert len(field) > 0, "The given array has no size"

    return len(field)

## A data handle used when loading data to be shown at a later point.
# \ingroup SLMDisplayPython
class Datahandle(ctypes.Structure):
    ## The fields of the data handle struct.
    _fields_ = [
        ("id",               ctypes.c_uint),
        ("state",            ctypes.c_uint8),
        ("errorCode",        ctypes.c_uint8),
        ("__padding__",      ctypes.c_uint8),
        ("durationInFrames", ctypes.c_uint8),
        ("showFlags",        ctypes.c_uint),
        ("phaseWrap",        ctypes.c_float),
        ("lookupTableID",    ctypes.c_uint),
        ("loadingTimeMs",    ctypes.c_ushort),
        ("conversionTimeMs", ctypes.c_ushort),
        ("processingTimeMs", ctypes.c_ushort),
        ("transferTimeMs",   ctypes.c_ushort),
        ("renderTimeMs",     ctypes.c_ushort),
        ("visibleTimeMs",    ctypes.c_ushort),
    ]

    ## Represents an action that did not happen yet or was not required.
    NotDone = 0xFFFF
    
    ## Destroys the data associated with this handle.
    def __del__(self):
        Datahandle.Release(self.id)

    ## Releases the data associated with a datahandle id. This function is not required when using the \ref Datahandle class instead of the ids.
    # \param datahandleid The id of the handle you want to release
    # \return No return value.
    @staticmethod
    def Release(datahandleid):
        if datahandleid > 0 and SLMDisplay.Instance is not None:
            SLMDisplay.Instance._library.heds_datahandle_release_id(datahandleid)

    ## Releases all data associated with handles. This function is not required when using the \ref Datahandle class instead of the ids.
    # \return No return value.
    @staticmethod
    def ReleaseAll():
        if SLMDisplay.Instance is not None:
            SLMDisplay.Instance._library.heds_datahandle_release_all()

    ## Ensures that when the datahandle is deleted, the associated data remains valid.
    # You must then use Datahandle.Release(handleid) to release the data.
    # \return The id associated with this handle.
    def retainData(self):
        id = self.id

        ## \cond IGNORE
        self.id = 0
        ## \endcond

        return id

## This class gives you access to the SLM Graphics Library and slm devices.
# \ingroup SLMDisplayPython
class SLMDisplay:
    from .heds_errorcodes import ErrorCode
    from .heds_showflags import ShowFlags
    from .heds_state import State

    ## The current Instance of the library.
    Instance = None

    ## Creates a new Instance of the library.
    # \param binaryFolder The folder where the binaries are stored. Expects a folder that contains "<platform>/holoeye_slmdisplaysdk.dll"
    def __init__(self, binaryFolder = ""):
        
        if binaryFolder == "":
            binaryFolder = os.getenv("HEDS_PYTHON", "")

            if binaryFolder == "":
                raise RuntimeError("The environmental variable HEDS_PYTHON is not set.")

        if not os.path.isdir(binaryFolder):
            raise RuntimeError("The binaries folder \"" + binaryFolder + "\" does not exist.")

        platform = "win32" if sys.maxsize == (2**31 - 1) else "win64"

        ## The path of the dynamic library file that was loaded.
        self.librarypath = os.path.abspath( os.path.join(binaryFolder, platform, "holoeye_slmdisplaysdk.dll") )

        if not os.path.isfile(self.librarypath):
            raise RuntimeError("Cannot find binary file \"" + self.librarypath + "\".")

        try:
            ## \cond INTERNALDOC
            ## The ctypes library object.
            self._library = ctypes.cdll.LoadLibrary(self.librarypath)
            ## \endcond

            # Correct some types
            self._library.heds_error_string.restype = ctypes.c_char_p

            class SlmSize(ctypes.Structure):
                _fields_ = [
                    ("width", ctypes.c_int),
                    ("height", ctypes.c_int)
                ]

            self._library.heds_slm_size_px.restype = SlmSize

            class SlmSizeMM(ctypes.Structure):
                _fields_ = [
                    ("width", ctypes.c_double),
                    ("height", ctypes.c_double)
                ]

            self._library.heds_slm_size_mm.restype = SlmSizeMM

            self._library.heds_slm_pixelsize_um.restype = ctypes.c_double
            self._library.heds_slm_pixelsize_m.restype = ctypes.c_double
            self._library.heds_slm_refreshrate_hz.restype = ctypes.c_float

            self._library.heds_slm_width_mm.restype = ctypes.c_double
            self._library.heds_slm_height_mm.restype = ctypes.c_double

            self._library.heds_show_dividedscreen_vertical.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_int)
            self._library.heds_show_dividedscreen_horizontal.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_int)

            self._library.heds_show_grating_vertical_blaze.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double)
            self._library.heds_show_grating_horizontal_blaze.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double)

            self._library.heds_show_phasefunction_axicon.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double)
            self._library.heds_show_phasefunction_lens.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double)
            self._library.heds_show_phasefunction_vortex.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double)

            self._library.heds_show_phasevalues_single.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_uint32, ctypes.c_float)
            self._library.heds_show_phasevalues_double.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_uint32, ctypes.c_float)

            self._library.heds_load_phasevalues_single.argtypes = (ctypes.POINTER(Datahandle), ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_float)
            self._library.heds_load_phasevalues_double.argtypes = (ctypes.POINTER(Datahandle), ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_float)

        except:
            raise RuntimeError("Failed to initialize library from \"" + self.librarypath + "\".")

        ## The refreshrate of the slm in Hz.
        self.refreshrate_hz = 0

        ## The pixelsize of the slm in micro-meters.
        self.pixelsize_um = 0

        ## The pixelsize of the slm in meters.
        self.pixelsize_m = 0

        ## The width of the slm in pixel.
        self.width_px = 0

        ## The height of the slm in pixel.
        self.height_px = 0

        ## The size of the slm in pixel.
        self.size_px = 0

        ## The width of the slm in pixel.
        self.width_mm = 0

        ## The height of the slm in pixel.
        self.height_mm = 0

        ## The size of the slm in millimeters.
        self.size_mm = 0

        SLMDisplay.Instance = self

        # Open the slm
        result = self.open()

        if result != SLMDisplay.ErrorCode.NoError:
            raise RuntimeError("The SLM Graphics Library was not initialized.")

    ## Destroys this instance of the library.
    # \return No return value.
    def release(self):
        if SLMDisplay.Instance is self:
            SLMDisplay.Instance = None

    ## \cond INTERNALDOC
    ## Checks if the given data is a data handle id.
    # \return True when \p data is a data handle id.
    @staticmethod
    def _isID(data):
        return isinstance(data, int) or (not isPython3 and isinstance(data, long)) or isinstance(data, ctypes.c_int) or isinstance(data, ctypes.c_uint)
    ## \endcond

    ## Provides an error string for a given error.
    # \param error The error code to provide the string for.
    # \return An error string for the given error. None when the given error is invalid.
    def errorString(self, error):
        return self._library.heds_error_string(error)

    ## Opens the slm window when not already open.
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    def open(self):
        err =  self._library.heds_init_slm()

        if err != SLMDisplay.ErrorCode.NoError:
            return err

        ## The refreshrate of the slm in Hz.
        self.refreshrate_hz = self._library.heds_slm_refreshrate_hz()

        ## The pixelsize of the slm in micro-meters.
        self.pixelsize_um = self._library.heds_slm_pixelsize_um()

        ## The pixelsize of the slm in meters.
        self.pixelsize_m = self.pixelsize_um / 1.0E6

        size = self._library.heds_slm_size_px()

        ## The width of the slm in pixel.
        self.width_px = size.width

        ## The height of the slm in pixel.
        self.height_px = size.height

        ## The size of the slm in pixel.
        self.size_px = (self.width_px, self.height_px)

        ## The width of the slm in pixel.
        self.width_mm = self.width_px * self.pixelsize_m * 1000

        ## The height of the slm in pixel.
        self.height_mm = self.height_px * self.pixelsize_m * 1000

        ## The size of the slm in millimeters.
        self.size_mm = (self.width_mm, self.height_mm)

        return SLMDisplay.ErrorCode.NoError

    ## Closes the slm window when open.
    # \return No return type.
    def close(self):
        self._library.heds_close_slm()

        self.refreshrate_hz = 0
        self.pixelsize_um = 0
        self.pixelsize_m = 0
        self.width_px = 0
        self.height_px = 0
        self.size_px = 0
        self.width_mm = 0
        self.height_mm = 0
        self.size_mm = 0

    ## Show or hide the SLM preview window. If SLM is not initialized, try to initialize before opening the preview window.
    # \param show When True the window will be shown. When False it will be closed.
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    def utilsSLMPreviewShow(self, show = True):
        return int(self._library.heds_utils_slm_preview_show(ctypes.c_int(show)))

    ## Shows a given image file on the slm.
    # \param imageFilePath A string containing the path to an image file.
    # <br>Supported image file formats are: bmp, cur, dds, gif, icns, ico, jpeg, jpg, pbm, pgm, png, ppm, svg, svgz, tga, tif, tiff, wbmp, webp, xbm, xpm.
    # <br>For holographic data, we recommend not to use any lossy compressed formats, like jpg. Instead please use uncompressed formats (e.g. bmp) or lossless compressed formats (e.g. png).
    # \param showFlags Flags that define how the data is shown on the slm.
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    # \see \ref imagefile_grayscale.py \ref imagefile_rgb.py
    def showDataFromFile(self, imageFilePath, showFlags = 0):
        abspath = os.path.abspath(imageFilePath)

        isUnicode = (isinstance(abspath, str)) if isPython3 else (isinstance(abspath, unicode))

        if isUnicode:
            if not os.path.exists(abspath):
                return SLMDisplay.ErrorCode.FileNotFound

            return self._library.heds_show_data_fromfile_unicode(abspath, showFlags)

        # we do not check if the file exists here because this would fail for utf-8 strings
        return self._library.heds_show_data_fromfile_utf8(abspath, showFlags)

    ## Shows data associated with a handle on the slm.
    # \param handleOrID A datahandle or a datahandle id.
    # \param showFlags Flags that define how the data is shown on the slm.
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    # \see \ref slideshow_data_preload.py
    def showDatahandle(self, handleOrID, showFlags=0):
        if isinstance(handleOrID, Datahandle):
            handleptr = ctypes.pointer(handleOrID)

            return self._library.heds_show_datahandle(handleptr, showFlags)

        if SLMDisplay._isID(handleOrID):
            return self._library.heds_show_datahandle_id(handleOrID, showFlags)

        return SLMDisplay.ErrorCode.InvalidHandle

    ## Shows arbitrary data on the slm.
    # \param data A ctypes or numpy data pointer.
    # \param showFlags Flags that define how the data is shown on the slm.
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    # \see \ref data_uint8.py \ref data_uint8_tiled.py \ref data_float.py \ref data_float_tiled.py \ref slideshow_data_show.py
    def showData(self, data, showFlags = 0):
        if supportNumPy and isinstance(data, numpy.ndarray):
            height = len(data)

            if height < 1:
                return SLMDisplay.ErrorCode.InvalidDataHeight

            width = len(data[0])

            if width < 1:
                return SLMDisplay.ErrorCode.InvalidDataWidth

            type = data.dtype.type

            if type is numpy.uint8:
                if len(data.shape) < 3:
                    return self._library.heds_show_data_grayscale_uchar(width, height, data.ctypes, showFlags)
                if len(data.shape) == 3:
                    if (data.shape[2] == 1):
                        return self._library.heds_show_data_grayscale_uchar(width, height, data.ctypes, showFlags)
                    if (data.shape[2] == 3):
                        return self._library.heds_show_data_rgb24(width, height, data.ctypes, showFlags)
                    if (data.shape[2] == 4):
                        return self._library.heds_show_data_rgba32(width, height, data.ctypes, showFlags)

            if type is numpy.uintc:
                return self._library.heds_show_data_rgba32(width, height, data.ctypes, showFlags)

            if type is numpy.single:
                return self._library.heds_show_data_grayscale_single(width, height, data.ctypes, showFlags)

            if type is numpy.double:
                return self._library.heds_show_data_grayscale_double(width, height, data.ctypes, showFlags)

        elif isinstance(data, ctypes.Array):
            height = len(data)

            if height < 1:
                return SLMDisplay.ErrorCode.InvalidDataHeight

            width = len(data[0])

            if width < 1:
                return SLMDisplay.ErrorCode.InvalidDataWidth

            type = data._type_._type_

            if type is ctypes.c_ubyte:
                return self._library.heds_show_data_grayscale_uchar(width, height, data, showFlags)

            if type is ctypes.c_uint:
                return self._library.heds_show_data_rgba32(width, height, data, showFlags)

            if type is ctypes.c_float:
                return self._library.heds_show_data_grayscale_single(width, height, data, showFlags)

            if type is ctypes.c_double:
                return self._library.heds_show_data_grayscale_double(width, height, data, showFlags)

        return SLMDisplay.ErrorCode.InvalidDataFormat

    ## Shows an array of phase values on the SLM. The unit of the phase values is the same as for \p phaseWrap. By default radians.
    # \param phaseValues The pointer to the given phase values. The unit of the phase values is radian.
    # \param showFlags Flags that define how the data is shown on the slm.
    # \param phaseWrap The phase wrap applied to the data, basically a modulo. A value of zero means there is no phase wrap applied.
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    # \see \ref phasevalues.py \ref phasevalues_tiled.py \ref axicon.py \see \ref axicon_fast.py
    def showPhasevalues(self, phaseValues, showFlags = 0, phaseWrap = 6.28318530718):
        if supportNumPy and isinstance(phaseValues, numpy.ndarray):
            height = len(phaseValues)

            if height < 1:
                return SLMDisplay.ErrorCode.InvalidDataHeight

            width = len(phaseValues[0])

            if width < 1:
                return SLMDisplay.ErrorCode.InvalidDataWidth

            type = phaseValues.dtype.type

            if type is numpy.single:
                return self._library.heds_show_phasevalues_single(width, height, ctypes.cast(phaseValues.ctypes, ctypes.POINTER(ctypes.c_float)), showFlags, phaseWrap)

            if type is numpy.double:
                return self._library.heds_show_phasevalues_double(width, height, ctypes.cast(phaseValues.ctypes, ctypes.POINTER(ctypes.c_double)), showFlags, phaseWrap)

        elif isinstance(phaseValues, ctypes.Array):
            height = len(phaseValues)

            if height < 1:
                return SLMDisplay.ErrorCode.InvalidDataHeight

            width = len(phaseValues[0])

            if width < 1:
                return SLMDisplay.ErrorCode.InvalidDataWidth

            type = phaseValues._type_._type_

            if type is ctypes.c_float:
                return self._library.heds_show_phasevalues_single(width, height, ctypes.cast(phaseValues, ctypes.POINTER(ctypes.c_float)), showFlags, phaseWrap)

            if type is ctypes.c_double:
                return self._library.heds_show_phasevalues_double(width, height, ctypes.cast(phaseValues, ctypes.POINTER(ctypes.c_double)), showFlags, phaseWrap)

        return SLMDisplay.ErrorCode.InvalidDataFormat

    ## Shows a blank screen with a constant gray value.
    # \param grayValue The gray value which is addressed to the full SLM. The value is automatically wrapped to the range 0-255.
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    # \see \ref builtin_blankscreen.py
    def showBlankscreen(self, grayValue = 128):
        return self._library.heds_show_blankscreen(grayValue)

    ## Shows two areas on the SLM with two different gray values. The function is intended to be used for phase measurements of the SLM in which one half of the SLM can be used as a reference to the other half.
    # The screen will be split along the vertical (y) axis. This means that the gray levels a and b are painted to the left and right side of the SLM, resp.
    # \param screenDivider The ratio by which the SLM screen should be divided. Meaningful values are between 0.0 and 1.0. [default value = 0.5]
    # \param a_gray_value The gray value which will be adressed on the first side of the SLM. Values are wrapped to 0-255 range. [default value = 0]
    # \param b_gray_value The gray value which will be adressed on the second side of the SLM. Values are wrapped to 0-255 range. [default value = 255]
    # \param flipped If set to true, the first side will addressed with \p b_gray_value and the second side will be set to a_gray_value. [default value = false]
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    # \see \ref builtin_dividedscreen.py
    def showDividedScreenVertical(self, a_gray_value = 0, b_gray_value = 255, screenDivider = 0.5, flipped = False):
        return self._library.heds_show_dividedscreen_vertical(a_gray_value, b_gray_value, screenDivider, flipped)

    ## Shows two areas on the SLM with two different gray values. The function is intended to be used for phase measurements of the SLM in which one half of the SLM can be used as a reference to the other half.
    # The screen will be split along the horizontal (x) axis. This means that the gray levels a and b are painted to the upper and lower side of the SLM, resp.
    # \param screenDivider The ratio by which the SLM screen should be divided. Meaningful values are between 0.0 and 1.0. [default value = 0.5]
    # \param a_gray_value The gray value which will be adressed on the first side of the SLM. Values are wrapped to 0-255 range. [default value = 0]
    # \param b_gray_value The gray value which will be adressed on the second side of the SLM. Values are wrapped to 0-255 range. [default value = 255]
    # \param flipped If set to true, the first side will addressed with \p b_gray_value and the second side will be set to a_gray_value. [default value = false]
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    # \see \ref builtin_dividedscreen.py
    def showDividedScreenHorizontal(self, a_gray_value = 0, b_gray_value = 255, screenDivider = 0.5, flipped = False):
        return self._library.heds_show_dividedscreen_horizontal(a_gray_value, b_gray_value, screenDivider, flipped)

    ## Shows a vertical binary grating. The grating consists of two gray values \p a_gray_value and \p b_gray_value which will be addressed to the SLM.
    # The gray values have the data type int and will be wrapped internally to an unsigned char with a range of 0 to 255.
    # The width of each area with the gray value \p a_gray_value and \p b_gray_value is defined by \p a_width and \p b_width, respectively.
    # Each pair of gray values is repeated so that the SLM is completely filled.
    # \param a_width The width of the first block with the value of \p a_gray_value. This parameter is mandatory.
    # \param b_width The width of the second block with the value of \p b_gray_value. This parameter is mandatory.
    # \param a_gray_value The addressed gray value of the first block. [default value = 0].
    # \param b_gray_value The addressed gray value of the second block. [default value = 128].
    # \param shift_x The horizontal offset applied to both blocks. [default value = 0].
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    # \see \ref builtin_grating_binary.py
    def showGratingVerticalBinary(self, a_width, b_width, a_gray_value = 0, b_gray_value = 128, shift_x = 0):
        return self._library.heds_show_grating_vertical_binary(a_width, b_width, a_gray_value, b_gray_value, shift_x)

    ## Shows a horizontal binary grating. The grating consists of two gray values \p a_gray_value and \p b_gray_value.
    # The gray values have the data type int and will be wrapped internally to an unsigned char with a range of 0 to 255.
    # Each pair of gray values is repeated so that the SLM is completely filled.
    # The width of each area with the gray value \p a_gray_value and \p b_gray_value is defined by \p a_width and \p b_width, respectively.
    # \param a_width The width of the first block with the value of \p a_gray_value. This parameter is mandatory.
    # \param b_width The width of the second block with the value of \p b_gray_value. This parameter is mandatory.
    # \param a_gray_value The addressed gray value of the first block. [default value = 0].
    # \param b_gray_value The addressed gray value of the second block. [default value = 128].
    # \param shift_y The vertical offset applied to both blocks. [default value = 0].
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    # \see \ref builtin_grating_binary.py
    def showGratingHorizontalBinary(self, a_width, b_width, a_gray_value = 0, b_gray_value = 128, shift_y = 0):
        return self._library.heds_show_grating_horizontal_binary(a_width, b_width, a_gray_value, b_gray_value, shift_y)

    ## Shows a vertical blazed grating on the SLM.
    # \param period The grating period in SLM pixels. The value is mandatory. Can be either positive or negative for an inverted grating profile. Please note that the phase can also be inverted by the \p phase_scale. If both values are negative, the invertions will superimpose to non invertion.
    # \param shift_x The horizontal offset applied to the grating. [default value = 0].
    # \param phase_scale Scales all phase values of this phase function. The value can be negative to invert the phase function. Other values than 1.0 and -1.0 are meant to optimize diffraction efficiency. Absolute values greater than 1.0 would lead to gray level saturation artifacts and are therefore limited to the range from -1.0 to +1.0. In case of limitation, a warning message will be shown. The scaling is done after wrapping phase values into the gray levels of the SLM. [default value = 1.0].
    # \param phase_offset Applies an offset to the phase values of this phase function. The unit of this value is in radian. The offset will retain the phase profile, but will change the actual used gray levels on the SLM. When this value is 0, the phase function will be centered into the gray value range on the SLM. After the offset was applied, wrapping to the gray values is done. [default value = 0.0].
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    # \see \ref builtin_grating_blaze.py
    def showGratingVerticalBlaze(self, period, shift_x = 0, phase_scale = 1.0, phase_offset = 0.0):
        return self._library.heds_show_grating_vertical_blaze(period, shift_x, phase_scale, phase_offset)

    ## Shows a horizontal blazed grating on the SLM.
    # \param period The grating period in SLM pixels. The value is mandatory. Can be either positive or negative for an inverted grating profile.
    # \param shift_y The vertical offset applied to the grating. [default value = 0].
    # \param phase_scale Scales all phase values of this phase function. The value can be negative to invert the phase function. Other values than 1.0 and -1.0 are meant to optimize diffraction efficiency. Absolute values greater than 1.0 would lead to gray level saturation artifacts and are therefore limited to the range from -1.0 to +1.0. In case of limitation, a warning message will be shown. The scaling is done after wrapping phase values into the gray levels of the SLM. [default value = 1.0].
    # \param phase_offset Applies an offset to the phase values of this phase function. The unit of this value is in radian. The offset will retain the phase profile, but will change the actual used gray levels on the SLM. When this value is 0, the phase function will be centered into the gray value range on the SLM. After the offset was applied, wrapping to the gray values is done. [default value = 0.0].
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    # \see \ref builtin_grating_blaze.py
    def showGratingHorizontalBlaze(self, period, shift_y = 0, phase_scale = 1.0, phase_offset = 0.0):
        return self._library.heds_show_grating_horizontal_blaze(period, shift_y, phase_scale, phase_offset)

    ## Shows an axicon. The phase has a conical shape.
    # \param inner_radius_px The radius in number of SLM pixel where the axicon phase function reached 2pi for the first time in respect to the center of the axicon.
    # \param center_x Horizontal shift of the center of the optical function on the SLM in number of pixel. [default value = 0].
    # \param center_y Vertical shift of the center of the optical function on the SLM in number of pixel. [default value = 0].
    # \param phase_scale Scales all phase values of this phase function. The value can be negative to invert the phase function. Other values than 1.0 and -1.0 are meant to optimize diffraction efficiency. Absolute values greater than 1.0 would lead to gray level saturation artifacts and are therefore limited to the range from -1.0 to +1.0. In case of limitation, a warning message will be shown. The scaling is done after wrapping phase values into the gray levels of the SLM. [default value = 1.0].
    # \param phase_offset Applies an offset to the phase values of this phase function. The unit of this value is in radian. The offset will retain the phase profile, but will change the actual used gray levels on the SLM. When this value is 0, the phase function will be centered into the gray value range on the SLM. After the offset was applied, wrapping to the gray values is done. [default value = 0.0].
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    # \see \ref builtin_axicon.py
    def showPhasefunctionAxicon(self, inner_radius_px, center_x = 0, center_y = 0, phase_scale = 1.0, phase_offset = 0.0):
        return self._library.heds_show_phasefunction_axicon(inner_radius_px, center_x, center_y, phase_scale, phase_offset)

    ## Shows a lens phase function. The phase has a parabolic shape.
    # The resulting focal length can be calculated as f [m] = (\p inner_radius_px * \p pixelsize_um * 1.0E-6) ^2 / (2.0*lambda),
    # with the incident optical wavelength lambda.
    # \param inner_radius_px The radius in number of SLM pixel where the lens phase function reached 2pi for the first time in respect to the center of the lens. This value is related to the focal length f of the lens phase function by f = (inner_radius_px * heds_slm_pixelsize())^2 / (2*lambda).
    # \param center_x Horizontal shift of the center of the optical function on the SLM in number of pixel. [default value = 0].
    # \param center_y Vertical shift of the center of the optical function on the SLM in number of pixel. [default value = 0].
    # \param phase_scale Scales all phase values of this phase function. The value can be negative to invert the phase function. Other values than 1.0 and -1.0 are meant to optimize diffraction efficiency. Absolute values greater than 1.0 would lead to gray level saturation artifacts and are therefore limited to the range from -1.0 to +1.0. In case of limitation, a warning message will be shown. The scaling is done after wrapping phase values into the gray levels of the SLM. [default value = 1.0].
    # \param phase_offset Applies an offset to the phase values of this phase function. The unit of this value is in radian. The offset will retain the phase profile, but will change the actual used gray levels on the SLM. When this value is 0, the phase function will be centered into the gray value range on the SLM. After the offset was applied, wrapping to the gray values is done. [default value = 0.0].
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    # \see \ref builtin_lens.py
    def showPhasefunctionLens(self, inner_radius_px, center_x = 0, center_y = 0, phase_scale = 1.0, phase_offset = 0.0):
        return self._library.heds_show_phasefunction_lens(inner_radius_px, center_x, center_y, phase_scale, phase_offset)

    ## Shows an optical vortex phase function on the SLM. The phase has a helical shape.
    # \param vortex_order The order of the optical vortex. If the order is one, the phase goes from 0 to 2pi over the full angle of 360 degree. For higher orders, 2pi phase shift is reached at angles of 360 degree divided by the given \p vortex_order. [default value = 1].
    # \param inner_radius_px The radius at the sigularity which will be set to gray value 0 on the SLM. [default value = 0].
    # \param center_x Horizontal shift of the center of the optical function on the SLM in number of pixel. [default value = 0].
    # \param center_y Vertical shift of the center of the optical function on the SLM in number of pixel. [default value = 0].
    # \param phase_scale Scales all phase values of this phase function. The value can be negative to invert the phase function. Other values than 1.0 and -1.0 are meant to optimize diffraction efficiency. Absolute values greater than 1.0 would lead to gray level saturation artifacts and are therefore limited to the range from -1.0 to +1.0. In case of limitation, a warning message will be shown. The scaling is done after wrapping phase values into the gray levels of the SLM. [default value = 1.0].
    # \param phase_offset Applies an offset to the phase values of this phase function. The unit of this value is in radian. The offset will retain the phase profile, but will change the actual used gray levels on the SLM. When this value is 0, the phase function will be centered into the gray value range on the SLM. After the offset was applied, wrapping to the gray values is done. [default value = 0.0].
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    # \see \ref builtin_vortex.py
    def showPhasefunctionVortex(self, vortex_order = 1, inner_radius_px = 0, center_x = 0, center_y = 0, phase_scale = 1.0, phase_offset = 0.0):
        return self._library.heds_show_phasefunction_vortex(vortex_order, inner_radius_px, center_x, center_y, phase_scale, phase_offset)

    ## \cond INTERNALDOC
    ## Generates an error with a handle
    @staticmethod
    def _handleError(error):
        h = Datahandle()
        h.state = SLMDisplay.State.Error;
        h.errorCode = error;

        return (error, h)
    ## \endcond

    ## Loads data to be displayed later.
    # \param data The data you want to load for the slm.
    # \return A tuple (errorCode, handle). You can check if errorCode is SLMDisplay.ErrorCode.NoError.
    # \see \ref slideshow_data_preload.py
    def loadData(self, data):
        handle = Datahandle()
        handleptr = ctypes.pointer(handle)

        if supportNumPy and isinstance(data, numpy.ndarray):
            height = len(data)

            if height < 1:
                return SLMDisplay._handleError(SLMDisplay.ErrorCode.InvalidDataHeight)

            width = len(data[0])

            if width < 1:
                return SLMDisplay._handleError(SLMDisplay.ErrorCode.InvalidDataWidth)

            type = data.dtype.type

            if type is numpy.uint8:
                if len(data.shape) < 3:
                    error = self._library.heds_load_data_grayscale_uchar(handleptr, width, height, data.ctypes)
                    return (error, handle)
                if len(data.shape) == 3:
                    if (data.shape[2] == 1):
                        error = self._library.heds_load_data_grayscale_uchar(handleptr, width, height, data.ctypes)
                        return (error, handle)
                    if (data.shape[2] == 3):
                        error = self._library.heds_load_data_rgb24(handleptr, width, height, data.ctypes)
                        return (error, handle)
                    if (data.shape[2] == 4):
                        error = self._library.heds_load_data_rgba32(handleptr, width, height, data.ctypes)
                        return (error, handle)
                

            if type is numpy.uintc:
                error = self._library.heds_load_data_rgba32(handleptr, width, height, data.ctypes)
                return (error, handle)

            if type is numpy.single:
                error = self._library.heds_load_data_grayscale_single(handleptr, width, height, data.ctypes)
                return (error, handle)

            if type is numpy.double:
                error = self._library.heds_load_data_grayscale_double(handleptr, width, height, data.ctypes)
                return (error, handle)

        elif isinstance(data, ctypes.Array):
            height = len(data)

            if height < 1:
                return SLMDisplay._handleError(SLMDisplay.ErrorCode.InvalidDataHeight)

            width = len(data[0])

            if width < 1:
                return SLMDisplay._handleError(SLMDisplay.ErrorCode.InvalidDataWidth)

            type = data._type_._type_

            if type is ctypes.c_ubyte:
                error = self._library.heds_load_data_grayscale_uchar(handleptr, width, height, data)
                return (error, handle)

            if type is ctypes.c_uint:
                error = self._library.heds_load_data_rgba32(handleptr, width, height, data)
                return (error, handle)

            if type is ctypes.c_float:
                error = self._library.heds_load_data_grayscale_single(handleptr, width, height, data)
                return (error, handle)

            if type is ctypes.c_double:
                error = self._library.heds_load_data_grayscale_double(handleptr, width, height, data)
                return (error, handle)

        return SLMDisplay._handleError(SLMDisplay.ErrorCode.UnsupportedDataFormat)

    ## Loads the given phase values to be shown on the SLM.
    # \param phaseValues The pointer to the given phase values.
    # \param phaseWrap The phase shift applied to the data. A value of zero means there is no phase shift applied.
    # \return A tuple (errorCode, handle). You can check if errorCode is SLMDisplay.ErrorCode.NoError.
    def loadPhasevalues(self, phaseValues, phaseWrap = 6.28318530718):
        handle = Datahandle()
        handleptr = ctypes.pointer(handle)

        if supportNumPy and isinstance(phaseValues, numpy.ndarray):
            height = len(phaseValues)

            if height < 1:
                return SLMDisplay._handleError(SLMDisplay.ErrorCode.InvalidDataHeight)

            width = len(phaseValues[0])

            if width < 1:
                return SLMDisplay._handleError(SLMDisplay.ErrorCode.InvalidDataWidth)

            type = phaseValues.dtype.type

            if type is numpy.single:
                error = self._library.heds_load_phasevalues_single(handleptr, width, height, ctypes.cast(phaseValues.ctypes, ctypes.POINTER(ctypes.c_float)), phaseWrap)
                return (error, handle)

            if type is numpy.double:
                error = self._library.heds_load_phasevalues_double(handleptr, width, height, ctypes.cast(phaseValues.ctypes, ctypes.POINTER(ctypes.c_double)), phaseWrap)
                return (error, handle)

        elif isinstance(phaseValues, ctypes.Array):
            height = len(phaseValues)

            if height < 1:
                return SLMDisplay._handleError(SLMDisplay.ErrorCode.InvalidDataHeight)

            width = len(phaseValues[0])

            if width < 1:
                return SLMDisplay._handleError(SLMDisplay.ErrorCode.InvalidDataWidth)

            type = phaseValues._type_._type_

            if type is ctypes.c_float:
                error = self._library.heds_load_phasevalues_single(handleptr, width, height, ctypes.cast(phaseValues, ctypes.POINTER(ctypes.c_float)), phaseWrap)
                return (error, handle)

            if type is ctypes.c_double:
                error = self._library.heds_load_phasevalues_double(handleptr, width, height, ctypes.cast(phaseValues, ctypes.POINTER(ctypes.c_double)), phaseWrap)
                return (error, handle)

        return SLMDisplay._handleError(SLMDisplay.ErrorCode.UnsupportedDataFormat)

    ## Loads data from a file.
    # \param imageFilePath The path to an image file you want to load.
    # <br>Supported image file formats are: bmp, cur, dds, gif, icns, ico, jpeg, jpg, pbm, pgm, png, ppm, svg, svgz, tga, tif, tiff, wbmp, webp, xbm, xpm.
    # <br>For holographic data, we recommend not to use any lossy compressed formats, like jpg. Instead please use uncompressed formats (e.g. bmp) or lossless compressed formats (e.g. png).
    # \return A tuple (errorCode, handle). You can check if errorCode is SLMDisplay.ErrorCode.NoError.
    def loadDataFromFile(self, imageFilePath):
        abspath = os.path.abspath(imageFilePath)

        isUnicode = (isinstance(abspath, str)) if isPython3 else (isinstance(abspath, unicode))

        handle = Datahandle()
        handleptr = ctypes.pointer(handle)

        if isUnicode:
            if not os.path.exists(abspath):
                return SLMDisplay._handleError(SLMDisplay.ErrorCode.FileNotFound)

            error = self._library.heds_load_data_fromfile_unicode(handleptr, abspath)
        else:
            # we do not check if the file exists here because this would fail for utf-8 strings
            error = self._library.heds_load_data_fromfile_utf8(handleptr, abspath)

        return (error, handle)

    ## Updates a handle with the latest information.
    # \param handle The handle we want to update.
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    def updateDatahandle(self, handle):
        if not isinstance(handle, Datahandle) or handle.id < 1:
            return SLMDisplay.ErrorCode.InvalidHandle

        handleptr = ctypes.pointer(handle)

        return self._library.heds_datahandle_update(handleptr)

    ## Changes the duration of a datahandle.
    # \param handle The handle we want to change.
    # \param durationInFrames The new duration.
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    def datahandleSetDuration(self, handle, durationInFrames):
        if not isinstance(handle, Datahandle) or handle.id < 1:
            return SLMDisplay.ErrorCode.InvalidHandle

        if durationInFrames < 1 or durationInFrames > 255:
            return SLMDisplay.ErrorCode.InvalidDurationInFrames

        handleptr = ctypes.pointer(handle)

        return self._library.heds_datahandle_set_duration(handleptr, durationInFrames)

    ## Changes the show flags of a datahandle.
    # \param handle The handle we want to change.
    # \param showFlags The new show flags.
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    def datahandleSetShowFlags(self, handle, showFlags):
        if not isinstance(handle, Datahandle) or handle.id < 1:
            return SLMDisplay.ErrorCode.InvalidHandle

        handleptr = ctypes.pointer(handle)

        return self._library.heds_datahandle_set_showflags(handleptr, showFlags)

    ## Assigns data as a lookup table for another.
    # \param handle The handle we want to assign the lookup table to.
    # \param lutHandle The handle of the lookup table. Must be one-dimensional data. Pass None to remove the lookup table again.
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    def datahandleSetLookupTable(self, handle, lutHandle):
        if not isinstance(handle, Datahandle) or handle.id < 1:
            return SLMDisplay.ErrorCode.InvalidHandle

        if (lutHandle is not None and not isinstance(handle, Datahandle)) or (isinstance(handle, Datahandle) and handle.id < 1):
            return SLMDisplay.ErrorCode.InvalidHandle

        handleptr = ctypes.pointer(handle)
        lutptr = ctypes.pointer(lutHandle)

        return self._library.heds_datahandle_set_lookuptable(handleptr, lutptr)

    ## Waits until a data handle has reached a certain state.
    # \param handle The handle we want to wait for.
    # \param state The state to wait for.
    # \param timeOutInMs The time in milliseconds to wait before returning with the error SLMDisplay.ErrorCode.WaitForHandleTimedOut.
    # \return SLMDisplay.ErrorCode.NoError when there is no error.
    def datahandleWaitFor(self, handle, state, timeOutInMs = 4000):
        if SLMDisplay._isID(handle):
            return self._library.heds_datahandle_waitfor_id(handle, state, timeOutInMs)

        if isinstance(handle, Datahandle):
            handleptr = ctypes.pointer(handle)

            return self._library.heds_datahandle_waitfor(handleptr, state, timeOutInMs)

        return SLMDisplay.ErrorCode.InvalidHandle
