package opp.DTO;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import opp.domain.BloodGroup;
import opp.domain.Organization;

public class BloodSupplyDTO {
    private Integer id;

    private Integer amount;

    @JsonIgnore
    private Organization organization;
    private String organizationNaziv;
    private String bloodType;
    @JsonIgnore
    private BloodGroup bloodGroup;

    public BloodSupplyDTO(Integer id, Integer amount, String organizationNaziv, String bloodType) {
        this.id = id;
        this.amount = amount;
        this.organizationNaziv = organizationNaziv;
        this.bloodType = bloodType;
    }
    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getAmount() {
        return amount;
    }

    public void setAmount(Integer amount) {
        this.amount = amount;
    }

    public Organization getOrganization() {
        return organization;
    }

    public void setOrganization(Organization organization) {
        this.organization = organization;
    }

    public BloodGroup getBloodGroup() {
        return bloodGroup;
    }

    public void setBloodGroup(BloodGroup bloodGroup) {
        this.bloodGroup = bloodGroup;
    }

    public String getOrganizationNaziv() {
        return organizationNaziv;
    }

    public void setOrganizationNaziv(String organizationNaziv) {
        this.organizationNaziv = organizationNaziv;
    }

    public String getBloodType() {
        return bloodType;
    }

    public void setBloodType(String bloodType) {
        this.bloodType = bloodType;
    }

    @Override
    public String toString() {
        return "BloodSupplyDTO{" +
                "id=" + id +
                ", amount=" + amount +
                '}';
    }
}