package opp.dao;

import opp.domain.BloodGroup;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.stereotype.Repository;

@Repository
@EnableJpaRepositories
public interface BloodGroupRepository extends JpaRepository<BloodGroup, Long> {
    BloodGroup findByBloodType(String selectedBloodGroup);
}
