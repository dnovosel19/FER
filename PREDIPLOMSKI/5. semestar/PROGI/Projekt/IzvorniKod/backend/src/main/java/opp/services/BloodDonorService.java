package opp.services;

import opp.DTO.BloodDonorDTO;
import opp.DTO.LoginDTO;
import opp.domain.Donor;
import org.springframework.http.ResponseEntity;

import java.util.Map;
import java.util.Optional;


public interface BloodDonorService {

	ResponseEntity<?> addBloodDonor(BloodDonorDTO bloodDonorDTO);

	void deleteDonorAndDonations(Long donorId);

	Optional<Donor> findByUsername(String username);

	Donor fetch(long donorId);

	Optional<Donor> findById(long groupId);
}
