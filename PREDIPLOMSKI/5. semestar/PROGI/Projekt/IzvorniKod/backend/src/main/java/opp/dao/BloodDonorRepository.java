package opp.dao;

import opp.domain.Donor;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
@EnableJpaRepositories
public interface BloodDonorRepository extends JpaRepository<Donor, Long> {
	Donor findByUsername(String username);

	Optional<Donor> findOneByUsernameAndPassword(String username, String password);

	Donor findByName(String name);

	int countByOib(String oib);

	int countByUsername(String username);

    Optional<Donor> findByUsernameAndIdNot(String newUsername, Long donorId);
}
