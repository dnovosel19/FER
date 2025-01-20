import { AxiosRequestConfig } from "axios";
import { UserData } from "./UserFunc";

export function getAuthent(): AxiosRequestConfig {
    return {
        auth: {
            username: String(getUsername()),
            password: String(getPassword())
        }
    };
}

export function getId(): number | null {
    let id = localStorage.getItem("id");
    if(id == null) {
        return id;
    }
    else {
        return +id;
    }
}

export function setId(id: number) {
    localStorage.setItem("id", String(id));
}

export function getUsername(): string | null {
    return localStorage.getItem("username");
}

export function setUsername(username: string) {
    localStorage.setItem("username", username);
}

export function getPassword(): string | null {
    return localStorage.getItem("password");
}

export function setPassword(password: string) {
    localStorage.setItem("password", password);
}

export function setUserData(user: UserData) {
    setId(user.id)
    setPassword(user.password)
    setUsername(user.username)
}