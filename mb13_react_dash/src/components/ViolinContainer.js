import React, {useState, useEffect, useRef} from 'react';

import {Box, Center, Grid, GridItem} from "@chakra-ui/react";

import ViolinChart from './D3/ViolinChart';
import { D3Container } from './D3Container';

export const ViolinContainer = ({data, title}) => {

    const violinRef = useRef();
    return (
        <Box w="100%" h="100%">
            <D3Container
                ref={violinRef}
                data={data}
                id={"voilin-" + title}
                viz={ViolinChart}
            />
        </Box>
    )
}