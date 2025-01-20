package opp.DTO;

import com.fasterxml.jackson.annotation.JsonIgnore;

import java.util.LinkedHashSet;
import java.util.Set;

public class OrganizationDTO {
    private Integer id;

    private String adminUsername;

    private String adminPassword;

    private String adminName;

    private String adminSurname;
    private Integer locationId;
    private Integer organizationTypeId;
    private String naziv;
    @JsonIgnore
    private Set<BloodSupplyDTO> bloodSupplies = new LinkedHashSet<>();
    public OrganizationDTO() {
    }

    public OrganizationDTO(Integer id, String adminUsername, String adminPassword, String adminName, String adminSurname, Integer locationId, Integer organizationTypeId, String naziv) {
        this.id = id;
        this.adminUsername = adminUsername;
        this.adminPassword = adminPassword;
        this.adminName = adminName;
        this.adminSurname = adminSurname;
        this.locationId = locationId;
        this.organizationTypeId = organizationTypeId;
        this.naziv = naziv;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getAdminUsername() {
        return adminUsername;
    }

    public void setAdminUsername(String adminUsername) {
        this.adminUsername = adminUsername;
    }

    public String getAdminPassword() {
        return adminPassword;
    }

    public void setAdminPassword(String adminPassword) {
        this.adminPassword = adminPassword;
    }

    public String getAdminName() {
        return adminName;
    }

    public void setAdminName(String adminName) {
        this.adminName = adminName;
    }

    public String getAdminSurname() {
        return adminSurname;
    }

    public void setAdminSurname(String adminSurname) {
        this.adminSurname = adminSurname;
    }

    public String getNaziv() {
        return naziv;
    }

    public void setNaziv(String naziv) {
        this.naziv = naziv;
    }

    public Integer getLocationId() {
        return locationId;
    }

    public void setLocationId(Integer locationId) {
        this.locationId = locationId;
    }

    public Integer getOrganizationTypeId() {
        return organizationTypeId;
    }

    public void setOrganizationTypeId(Integer organizationTypeId) {
        this.organizationTypeId = organizationTypeId;
    }

    public Set<BloodSupplyDTO> getBloodSupplies() {
        return bloodSupplies;
    }

    public void setBloodSupplies(Set<BloodSupplyDTO> bloodSupplies) {
        this.bloodSupplies = bloodSupplies;
    }

    @Override
    public String toString() {
        return "OrganizationDTO{" +
                "id=" + id +
                ", adminUsername='" + adminUsername + '\'' +
                ", adminPassword='" + adminPassword + '\'' +
                ", adminName='" + adminName + '\'' +
                ", adminSurname='" + adminSurname + '\'' +
                ", naziv='" + naziv + '\'' +
                '}';
    }

}