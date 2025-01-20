import axios, { AxiosRequestConfig } from "axios";
import { Login } from "../models/Login";
import { Register } from "./RegisterFunc";

export interface UserData {
    id: number,
    username: string,
    password: string,
    errorMessage?: string
}

export const loginUser = (login: Login): Promise<UserData> => {
    const loginPackage: AxiosRequestConfig = {
        auth: {
            username: String(login.username),
            password: String(login.password)
        }
    }
     return axios.post("/api/blood_donor/login", loginPackage)
            .then((response) => response.data)
            .catch((error) => {
                if (error.response && error.response.status === 401) {
                    throw new Error('Wrong username or password.');
                } else {
                    throw new Error('An error occurred during login.');
                }
            });
}

export const registerUser = (register: Register): Promise<UserData> => {
    console.log("register user");
    return axios.post('/api/register', register).then(e => e.data)
}

export const getUser = (id: string): Promise<UserData> => {
    return axios.get("/api/blood_donor/getInfo/" + id).then(e => e.data)
}

export const loginOrganization = (login: Login): Promise<UserData> => {
    const loginPackage: AxiosRequestConfig = {
        auth: {
            username: String(login.username),
            password: String(login.password)
        }
    };

    return axios.post("/api/organizations/login", loginPackage)
        .then((response) => response.data)
        .catch((error) => {
            if (error.response && error.response.status === 401) {
                throw new Error('Wrong username or password.');
            } else {
                throw new Error('An error occurred during login.');
            }
        });
};

export const registerOrganization = (register: Register): Promise<UserData> => {
    return axios.post('/api/registerOrganization', register).then(e => e.data)
}

export const getOrganization = (id: string): Promise<UserData> => {
    return axios.get("/api/user/getInfo/" + id).then(e => e.data)
}