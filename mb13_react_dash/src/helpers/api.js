import axios from "axios"

const url = "http://localhost:8001"


export const get_rf_data = () => {
    const config = {
        method: "get",
        url: url + "/rf_gain"
    }

    return axios(config).then(response => response.data.data)
}

export const get_failure_types = () => {
    const config = {
        method: "get",
        url: url + "/failure_types"
    }

    return axios(config).then(response => response.data.data)
}