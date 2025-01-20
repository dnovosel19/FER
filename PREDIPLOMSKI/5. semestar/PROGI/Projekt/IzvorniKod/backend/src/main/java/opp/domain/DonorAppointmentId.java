package opp.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import org.hibernate.Hibernate;

import java.io.Serial;
import java.io.Serializable;
import java.util.Objects;

@Embeddable
public class DonorAppointmentId implements Serializable {
	@Serial
	private static final long serialVersionUID = 7618467483171697775L;
	@Column(name = "iddonor", nullable = false)
	private Integer iddonor;

	@Column(name = "idtermin", nullable = false)
	private Integer idtermin;
	public DonorAppointmentId() {
	}

	public DonorAppointmentId(Integer iddonor, Integer idtermin) {
		this.iddonor = iddonor;
		this.idtermin = idtermin;
	}

	public Integer getIddonor() {
		return iddonor;
	}

	public void setIddonor(Integer iddonor) {
		this.iddonor = iddonor;
	}

	public Integer getIdtermin() {
		return idtermin;
	}

	public void setIdtermin(Integer idtermin) {
		this.idtermin = idtermin;
	}

	@Override
	public boolean equals(Object o) {
		if (this == o) return true;
		if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o)) return false;
		DonorAppointmentId entity = (DonorAppointmentId) o;
		return Objects.equals(this.iddonor, entity.iddonor) &&
				Objects.equals(this.idtermin, entity.idtermin);
	}

	@Override
	public int hashCode() {
		return Objects.hash(iddonor, idtermin);
	}

}