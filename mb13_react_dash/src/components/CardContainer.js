import React from "react";

import {Box, Center, Text, VStack, Flex} from "@chakra-ui/react";

export const CardContainer = ({title, children, height}) => {

    return (
        <Box
            border="1px solid #000"
            boxShadow="5px 5px 5px 5px #343434"
            bg="#fff"
            borderRadius="10px"
            px={[0,"20px"]}
            w="100%"
            h={height ? height : "100%"}
        >
            {title ?
                <Flex justify="space-between" w="100%" >
                    <Text fontWeight={700} fontSize={["24px","26px"]} lineHeight="26px" py="0px" my="5px"> {title} </Text>
                </Flex>
                : null
            }
            {children}
        </Box>
    )
}