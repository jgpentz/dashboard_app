import React, {useState, useEffect} from "react";

import { Box, Text, Center, Grid, GridItem, Flex, Spinner } from "@chakra-ui/react";
import { LineChart } from "../components/LineChart";
import { GroupedBarChart } from "../components/GroupedBarChart";
import { StackedBarChart } from "../components/StackedBarChart";
import { DonutChart } from "../components/DonutChart";
import { get_failure_types, get_rf_data } from "../helpers/api";
import { ViolinContainer } from "../components/ViolinContainer";
import { Table } from "../components/Table";
import faker from "faker";
import { CardContainer } from "../components/CardContainer";







export const MB13 = ({title}) => {
    const [gainData, setGainData] = useState({});
    const [fTData, setfTData] = useState([]);
    const [tableData, setTableData] = useState([])

    const fetch_rf_data = async () => {
        let response = await get_rf_data();
        setGainData(response);    // TODO: add error checking that this data is sanitized
    }

    const fetch_ft_data = async () => {
        let response = await get_failure_types();
        setfTData(response);    // TODO: add error checking that this data is sanitized
    }

    useEffect(() => {
        fetch_rf_data();
        fetch_ft_data();

        createRandom();

        // const interval = setInterval(() => {
        //     fetch_rf_data();
        // }, 5000);
        // return() => clearInterval(interval);
    }, [])

    const createRandom = () => {
        let arr = []
        for (var i=0; i < 10; i++){
            arr.push({
                step: "Test",
                volume: Math.round(Math.random() * 20)
            })
        }
        setTableData(arr);
    }

    return (
        <Grid
            w="100%"
            h="100%"
            px="20px"
            py="20px"
            templateColumns={"repeat(12, 1fr)"}
            templateRows={"repeat(16, 1fr)"}
            rowGap="20px"
            columnGap={"20px"}

        >
            <GridItem colSpan={12} rowSpan={1} px="10px" py="10px" borderBottom={"1px solid #545454"}>
                <Text fontSize="28px" fontWeight={500}>
                    {title}
                </Text>
            </GridItem>
            <GridItem colSpan={4} rowSpan={5} >
                <LineChart />
            </GridItem>
            <GridItem colSpan={4} rowSpan={5} >
                <Table data={tableData}/>
            </GridItem>
            <GridItem colSpan={4} rowSpan={5} >
                <GroupedBarChart />
            </GridItem>

            <GridItem colSpan={3} rowSpan={5} >
                <StackedBarChart />
            </GridItem>
            <GridItem colSpan={3} rowSpan={5} >
                <ViolinContainer data={gainData.rx_br} title="rx_br"/>
            </GridItem>
            <GridItem colSpan={3} rowSpan={5} >
                <ViolinContainer data={gainData.rx_fw} title="rx_fw"/>
            </GridItem>
            <GridItem colSpan={3} rowSpan={5} >
                {/* <CardContainer title="RX Gain " h="100%"> */}
                    <ViolinContainer data={gainData.rx2_br} title="rx_br"/>
                {/* </CardContainer> */}
            </GridItem>
            <GridItem colSpan={3} rowSpan={5} >
                {fTData.length ?
                    <DonutChart data={fTData} />
                    :
                    // TODO move spinner to its' own component to use throughout project
                    <Center w="100%" h="100%">
                        <Spinner
                            size="md"
                            speed="0.65s"
                            color="blue.500"
                            thickness="4px"
                        />
                    </Center>
                }

            </GridItem>
            <GridItem colSpan={3} rowSpan={5} >
                <ViolinContainer data={gainData.rx2_fw} title="rx2_fw"/>
            </GridItem>
            <GridItem colSpan={3} rowSpan={5} >
                <ViolinContainer data={gainData.tx_br} title="tx_br"/>
            </GridItem>
            <GridItem colSpan={3} rowSpan={5} >
                <ViolinContainer data={gainData.tx_fw} title="tx_fw"/>
            </GridItem>
        </Grid>
    )

}
