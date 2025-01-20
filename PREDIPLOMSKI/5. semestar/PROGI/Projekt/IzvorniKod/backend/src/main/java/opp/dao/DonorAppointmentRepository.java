package opp.dao;

import opp.domain.DonorAppointment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
@EnableJpaRepositories
public interface DonorAppointmentRepository extends JpaRepository<DonorAppointment, Long> {
    DonorAppointment findByDonor_Id(Integer id);

    boolean existsByDonor_Id(Integer donorId);
}
