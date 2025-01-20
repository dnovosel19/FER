package opp.domain;

import jakarta.persistence.*;

@Entity
@Table(name = "zalihakrvi")
public class BloodSupply {
    @Id
    @Column(name = "idzaliha", nullable = false)
    private Integer id;

    @Column(name = "\"količina\"", nullable = false)
    private Integer amount;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "idustanova", nullable = false)
    private Organization organization;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "idgrupa", nullable = false)
    private BloodGroup bloodGroup;

    public BloodSupply() {
    }

    public BloodSupply(Integer id, Integer amount, Organization organization, BloodGroup bloodGroup) {
        this.id = id;
        this.amount = amount;
        this.organization = organization;
        this.bloodGroup = bloodGroup;
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

    @Override
    public String toString() {
        return "BloodSupply{" +
                "id=" + id +
                ", amount=" + amount +
                '}';
    }
}