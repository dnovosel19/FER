import axios, { AxiosRequestConfig } from "axios"
import { Login } from "../models/Login"
import { UserData } from "./UserFunc"

export interface Register {
    name: string,
    surname: string,
    username: string,
    oib: string,
    password: string
}
export interface RegisterOrganization {
    adminUsername: string,
    adminPassword: string,
    adminName: string,
    adminSurname: string,
    locationId: number
    organizationTypeId: number,
    naziv: string
}

export function jeBroj(pin: string): boolean {
    return /^\d+$/.test(pin);
}



export const registerUser = (register: Register): Promise<any> => {
    return axios.post("/api/blood_donor/register", register);
}

export const loginUser = (login: Login): Promise<UserData> => {
    const loginInf: AxiosRequestConfig = {
        auth: {
            username: String(login.username),
            password: String(login.password),
        },
    };
    return axios.post("/api/blood_donor/login", {}, loginInf).then(e => e.data);
}

export const loginOrganization = (login: Login): Promise<UserData> => {
    const  loginInf: AxiosRequestConfig = {
        auth: {
            username: String(login.username),
            password: String(login.password)
        }
    }
    return axios.get('/login', loginInf).then(e => e.data)
}

export const registerOrganization = (register: RegisterOrganization): Promise<any> => {
    return axios.post("/api/organization/registerOrganization", register)
        .then((response) => response.data)
        .catch((error) => {
            console.error("Error registering organization:", error.response);
            throw error;
        });
};
