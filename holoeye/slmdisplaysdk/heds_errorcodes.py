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


## \ingroup SLMDisplayPython
## The code for any error that occured.
class ErrorCode:

    ## No error.
    NoError = 0

    ## The slm was locked or disconnected.
    SLMUnavailable = 1

    ## The given filename is zero or too long.
    InvalidFilename = 2

    ## A filename was given, but the file does not exist.
    FileNotFound = 3

    ## A filename was given and the file exists, but the file format is not supported.
    UnsupportedFileFormat = 4

    ## The given data is zero or too long.
    InvalidDataPointer = 5

    ## The given data has a width less than one.
    InvalidDataWidth = 6

    ## The given data has a height less than one.
    InvalidDataHeight = 7

    ## A valid and supported filename or data was given, but the contained format is not supported. For example unsupported compressed gpu textures.
    UnsupportedDataFormat = 8

    ## The renderer had an internal error, for example when updating the window or sprite.
    InternalRendererError = 9

    ## There is not enough system memory left to process the given filename or data.
    OutOfSystemMemory = 10

    ## There is not enough video memory left to transfer the data to the gpu.
    OutOfVideoMemory = 11

    ## The current handle is invalid.
    InvalidHandle = 12

    ## The provided duration in frames is less than one or higher than 255.
    InvalidDurationInFrames = 13

    ## The given phase wrap must be greater than zero.
    InvalidPhaseWrap = 14

    ## Waiting for a datahandle to reach a certain state timed out and failed.
    WaitForHandleTimedOut = 15

    ## The given lookup table is not one-dimensional.
    InvalidLookupTableSize = 16

    ## The given lookup table contains phase values.
    InvalidLookupTableFormat = 17

    ## The given lookup table has an error, is assigned to itself or has another lookup table assigned.
    InvalidLookupHandleAssignment = 18


    ## The given data was not a two-dimensional array.
    InvalidDataDimensions = 100

    ## The provided value for width_a is zero or less.
    GratingWidthAInvalid = 101

    ## The provided value for width_b is zero or less.
    GratingWidthBInvalid = 102



