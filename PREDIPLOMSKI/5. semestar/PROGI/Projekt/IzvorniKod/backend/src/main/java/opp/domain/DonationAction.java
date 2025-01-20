package opp.domain;

import jakarta.persistence.*;

import java.time.LocalDate;
import java.util.LinkedHashSet;
import java.util.Set;

@Entity
@Table(name = "akcijadarivanja")
public class DonationAction {
	@Id
	@Column(name = "idakcija", nullable = false)
	private Integer id;

	@Column(name = "datumpocetka", nullable = false)
	private LocalDate startDate;

	@Column(name = "datumkraja", nullable = false)
	private LocalDate endDate;

	@ManyToOne(fetch = FetchType.LAZY, optional = false)
	@JoinColumn(name = "idlokacije", nullable = false)
	private Location location;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "idustanova")
	private Organization organization;

	@OneToMany(mappedBy = "donationAction")
	private Set<Appointment> appointments = new LinkedHashSet<>();

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public LocalDate getStartDate() {
		return startDate;
	}

	public void setStartDate(LocalDate startDate) {
		this.startDate = startDate;
	}

	public LocalDate getEndDate() {
		return endDate;
	}

	public void setEndDate(LocalDate endDate) {
		this.endDate = endDate;
	}

	public Location getLocation() {
		return location;
	}

	public void setLocation(Location location) {
		this.location = location;
	}

	public Organization getOrganization() {
		return organization;
	}

	public void setOrganization(Organization organization) {
		this.organization = organization;
	}

	public Set<Appointment> getAppointments() {
		return appointments;
	}

	public void setAppointments(Set<Appointment> appointments) {
		this.appointments = appointments;
	}
}