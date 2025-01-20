package opp.dao;

import opp.domain.Donation;
import opp.domain.Donor;
import opp.domain.Organization;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Map;
import java.util.Optional;

public interface DonationsRepository extends JpaRepository<Donation, Long> {
    List<Donation> findByDonor(Donor bloodDonor);

    Optional<Donation> findByOrganizationAndDonor(Organization organization, Donor bloodDonor);

//    Optional<Donation> findByBloodDonorAndOrganizationAndStatusNotIn(Donor bloodDonor, Organization organization, List<String> accepted);
    @Modifying
    @Query("DELETE FROM Donation d WHERE d.donor.id = :iddonor AND d.organization.id = :idustanova")
    void removeDonationByDonorIdAndOrganizationId(
            @Param("iddonor") Integer donorId,
            @Param("idustanova") Long organizationId
    );

    List<Donation> findReservedDonationsByDonorId(Long donorId);
    List<Donation> findByOrganization(Organization organization);

    Donation findTopByDonorOrderByTimeDesc(Donor donor);

    void deleteByDonorId(Long donorId);

    boolean existsByDonor(Donor bloodDonor);

    @Query("SELECT d.donor.id as donorId, COUNT(d) as donationCount FROM Donation d GROUP BY d.donor.id")
    List<Map<Donor, Object>> countDonationsPerDonor();

    boolean existsByDonor_Id(Integer donorId);
}
