package opp.domain;

import jakarta.persistence.*;

import java.time.LocalDate;
import java.util.LinkedHashSet;
import java.util.Set;

@Entity
@Table(name = "termin")
public class Appointment {
	@Id
	@Column(name = "idtermin", nullable = false)
	private Integer id;

	@Column(name = "\"vrijemepoč\"", nullable = false)
	private LocalDate startTime;

	@Column(name = "vrijemekraj", nullable = false)
	private LocalDate endTime;

	@ManyToOne(fetch = FetchType.LAZY, optional = false)
	@JoinColumn(name = "idakcija", nullable = false)
	private DonationAction donationAction;

	@OneToMany(mappedBy = "appopintment")
	private Set<DonorAppointment> donorAppointments = new LinkedHashSet<>();

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public LocalDate getStartTime() {
		return startTime;
	}

	public void setStartTime(LocalDate startTime) {
		this.startTime = startTime;
	}

	public LocalDate getEndTime() {
		return endTime;
	}

	public void setEndTime(LocalDate endTime) {
		this.endTime = endTime;
	}

	public DonationAction getDonationAction() {
		return donationAction;
	}

	public void setDonationAction(DonationAction donationAction) {
		this.donationAction = donationAction;
	}

	public Set<DonorAppointment> getDonorAppointments() {
		return donorAppointments;
	}

	public void setDonorAppointments(Set<DonorAppointment> donorAppointments) {
		this.donorAppointments = donorAppointments;
	}
}