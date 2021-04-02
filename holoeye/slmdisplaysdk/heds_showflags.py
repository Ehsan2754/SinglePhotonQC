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
## A list of available  show flags.
class ShowFlags:

    ## Shows two-dimensional data unscaled at the center of the slm. One-dimensional data is shown as a grating.
    PresentAutomatic = 0

    ## The data is shown unscaled at the center of the slm.
    #  Free areas are filled with zeroes. The data is cropped to the slm size.
    PresentCentered = 1

    ## If set, the slm will fit the slm so all data is visible and the aspect ratio is kept.
    #  Free areas on the top/bottom or left/right will be filled with zeroes.
    #  Only one of the present flags may be set.
    PresentFitWithBars = 2

    ## If set, the data will fit the slm so the slm is completely filled with data but the aspect ratio is kept.
    #  Some data might not be visible. Only one of the present flags may be set.
    PresentFitNoBars = 4

    ## If set, the data will completely fill the slm. The aspect ratio will not be kept.
    #  In short the data is shown fullscreen. Only one of the present flags may be set.
    PresentFitScreen = 8

    ## Shows the given data in a tiling pattern. The pattern is tiled around the center of the slm.
    PresentTiledCentered = 16

    ## If set, the rows and columns will be switched.
    TransposeData = 32

