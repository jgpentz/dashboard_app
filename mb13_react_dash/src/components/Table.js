import React, {useEffect, useState} from "react";
import {Box, Center, Flex, Grid, GridItem, Text} from "@chakra-ui/react";


export const Table = ({title, data}) => {


    const rows = data.map((d,i)=>
        <GridItem colSpan={1} rowSpan={1} key={"table-row" + i} >
            <Flex
                justify={"space-between"}
                w="100%"
                h="100%"
                border="1px solid #000"

            >
                <Box w="70%" h="100%" borderRight={"1px solid #000"}  px="10px">
                    <Text fontSize={"18px"}>
                        {d.step}
                    </Text>
                </Box>
                <Box w="30%" h="100%" textAlign={"end"} px="10px">
                    <Text fontSize={"18px"}>
                        {d.volume}
                    </Text>
                </Box>
            </Flex>
        </GridItem>
    )

    return(
        <Grid
            w="100%"
            h="100%"
            px="20px"
            py="20px"
            templateColumns={"repeat(1, 1fr)"}
            templateRows={"repeat(10, 1fr)"}
        >
            {rows}
        </Grid>
    )
}