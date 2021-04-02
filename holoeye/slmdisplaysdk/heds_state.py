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
## The current state of the data.
class State:

    ## The given filename or data is waiting for processing.
    WaitingForProcessing = 0

    ## The given filename is being loaded.
    LoadingFile = 1

    ## The given or loaded data needs to be converted. Performance Warning!
    ConvertingData = 2

    ## The data is being processed for display. This is not about conversion but about processing the data.
    ProcessingData = 3

    ## The data is waiting to be transferred to the gpu.
    WaitingForTransfer = 4

    ## The data is uploaded to the gpu.
    TransferringData = 5

    ## The data is ready to be rendered.
    ReadyToRender = 6

    ## The data is being rendered. This is about the actual effort needed to render the data.
    Rendering = 7

    ## The data is currently visible on the slm.
    Visible = 8

    ## The data has been shown and is now no longer visible.
    Finished = 9

    ## An error occured. Check error code.
    Error = 10

