package opp.DTO;

public class DonorDetailsDTO {

    private String username;
    private String bloodType;
    private String name;
    private String surname;
    private String oib;

    public DonorDetailsDTO() {
    }

    public DonorDetailsDTO(String username, String bloodType, String name, String surname, String oib) {
        this.username = username;
        this.bloodType = bloodType;
        this.name = name;
        this.surname = surname;
        this.oib = oib;
    }


    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getBloodType() {
        return bloodType;
    }

    public void setBloodType(String bloodType) {
        this.bloodType = bloodType;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getSurname() {
        return surname;
    }

    public void setSurname(String surname) {
        this.surname = surname;
    }

    public String getOib() {
        return oib;
    }

    public void setOib(String oib) {
        this.oib = oib;
    }
}
