package opp.domain;

import jakarta.persistence.*;

import java.time.LocalDate;

@Entity
@Table(name = "donacija")
public class Donation {
    @Id
    @GeneratedValue
    @Column(name = "iddonacija", nullable = false)
    private Integer id;

    @Column(name = "vrijeme", nullable = false)
    private LocalDate time;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "iddonor", nullable = false)
    private Donor donor;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "idlokacija", nullable = false)
    private Location location;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "idgrupa", nullable = false)
    private BloodGroup bloodGroup;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "idustanova", nullable = false)
    private Organization organization;

    public Donation() {
        this.time = LocalDate.now();
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public LocalDate getTime() {
        return time;
    }

    public void setTime(LocalDate time) {
        this.time = time;
    }

    public Donor getDonor() {
        return donor;
    }

    public void setDonor(Donor donor) {
        this.donor = donor;
    }

    public Location getLocation() {
        return location;
    }

    public void setLocation(Location location) {
        this.location = location;
    }

    public BloodGroup getBloodGroup() {
        return bloodGroup;
    }

    public void setBloodGroup(BloodGroup bloodGroup) {
        this.bloodGroup = bloodGroup;
    }

    public Organization getOrganization() {
        return organization;
    }

    public void setOrganization(Organization organization) {
        this.organization = organization;
    }

}