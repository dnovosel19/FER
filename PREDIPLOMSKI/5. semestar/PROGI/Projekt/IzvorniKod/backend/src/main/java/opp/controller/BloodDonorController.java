package opp.controller;

import opp.DTO.BloodDonorDTO;
import opp.dao.BloodDonorRepository;
import opp.domain.Donor;
import opp.services.BloodDonorService;
import opp.services.RequestDeniedException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.annotation.Secured;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/blood_donor")
public class BloodDonorController {
    @Autowired
    private BloodDonorService bloodDonorService;
    @Autowired
    private BloodDonorRepository bloodDonorRepository;

    @RequestMapping(value = "/register", method = {RequestMethod.POST, RequestMethod.OPTIONS})
    public ResponseEntity<?> registerBloodDonor(@RequestBody BloodDonorDTO bloodDonorDTO) {
        ResponseEntity<?> responseEntity = bloodDonorService.addBloodDonor(bloodDonorDTO);

        if (responseEntity.getStatusCode() == HttpStatus.OK) {
            return ResponseEntity.ok(Map.of("userType", "donor", "id", responseEntity.getBody()));
        } else if (responseEntity.getStatusCode() == HttpStatus.BAD_REQUEST) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(responseEntity.getBody());
        } else {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error during registration");
        }
    }

    @Secured("ROLE_USER")
    @GetMapping("/donorInformation/{donorId}")
    public ResponseEntity<Donor> getDonorInformation(@PathVariable Long donorId, @AuthenticationPrincipal CustomUserDetails u) {


		checkAllowedToEdit(donorId, u.getUsername());
        try {
            Donor donor = bloodDonorRepository.findById(donorId)
                    .orElseThrow(() -> new RuntimeException("Donor not found for id: " + donorId));

            return ResponseEntity.ok(donor);
        } catch (Exception e) {
            System.err.println("Error retrieving donor information: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }
	@Secured("ROLE_USER")
    @PutMapping("/changeName/{donorId}")
    public ResponseEntity<?> updateDonorName(@PathVariable Long donorId, @RequestBody Map<String, String> request, @AuthenticationPrincipal CustomUserDetails u) {
		checkAllowedToEdit(donorId, u.getUsername());

        String oldName = request.get("oldName");
        String newName = request.get("newName");
        System.out.println(" " + oldName + " " + newName);
        try {
            Donor donor = bloodDonorRepository.findById(donorId)
                    .orElseThrow(() -> new RuntimeException("Donor not found for id: " + donorId));

            donor.setName(newName);
            bloodDonorRepository.save(donor);

            return ResponseEntity.ok("Name updated successfully");
        } catch (Exception e) {
            System.err.println("Error updating donor name: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error updating donor name");
        }
    }
    @Secured("ROLE_USER")
	@PutMapping("/changeUsername/{donorId}")
    public ResponseEntity<?> updateDonorUsername(@PathVariable Long donorId, @RequestBody Map<String, String> request, @AuthenticationPrincipal CustomUserDetails u) {
		checkAllowedToEdit(donorId, u.getUsername());
        String oldUsername = request.get("oldUsername");
        String newUsername = request.get("newUsername");
        System.out.println(" " + oldUsername + " " + newUsername);

        try {
            // Check if the new username already exists for a different donor
            Optional<Donor> donorWithSameUsername = bloodDonorRepository.findByUsernameAndIdNot(newUsername, donorId);
            if (donorWithSameUsername.isPresent()) {
                System.out.println("Username already exists for another donor");
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Username already exists for another donor");
            }

            Donor donor = bloodDonorRepository.findById(donorId)
                    .orElseThrow(() -> new RuntimeException("Donor not found for id: " + donorId));

            donor.setUsername(newUsername);
            bloodDonorRepository.save(donor);

            return ResponseEntity.ok("Username updated successfully");
        } catch (Exception e) {
            System.err.println("Error updating donor username: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error updating donor username");
        }
    }
    @Secured("ROLE_USER")
	@PutMapping("/changePassword/{donorId}")
    public ResponseEntity<?> updateDonorPassword(@PathVariable Long donorId, @RequestBody Map<String, String> request, @AuthenticationPrincipal CustomUserDetails u) {
		checkAllowedToEdit(donorId, u.getUsername());
        String oldPassword = request.get("oldPassword");
        String newPassword = request.get("newPassword");

        try {
            Donor donor = bloodDonorRepository.findById(donorId)
                    .orElseThrow(() -> new RuntimeException("Donor not found for id: " + donorId));

            if (!donor.getPassword().equals(oldPassword)) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Incorrect old password");
            }

            donor.setPassword(newPassword);
            bloodDonorRepository.save(donor);

            return ResponseEntity.ok("Password updated successfully");
        } catch (Exception e) {
            System.err.println("Error updating donor password: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error updating donor password");
        }
    }
    @Secured("ROLE_USER")
	@PutMapping("/changeSurname/{donorId}")
    public ResponseEntity<?> updateDonorSurname(@PathVariable Long donorId, @RequestBody Map<String, String> request, @AuthenticationPrincipal CustomUserDetails u) {
		checkAllowedToEdit(donorId, u.getUsername());
        String oldSurname = request.get("oldSurname");
        String newSurname = request.get("newSurname");

        try {
            Donor donor = bloodDonorRepository.findById(donorId)
                    .orElseThrow(() -> new RuntimeException("Donor not found for id: " + donorId));

            if (!donor.getSurname().equals(oldSurname)) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Incorrect old surname");
            }

            donor.setSurname(newSurname);
            bloodDonorRepository.save(donor);

            return ResponseEntity.ok("Surname updated successfully");
        } catch (Exception e) {
            System.err.println("Error updating donor surname: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error updating donor surname");
        }
    }
    @Secured("ROLE_USER")
	@DeleteMapping("/deleteAccount/{donorId}")
    public ResponseEntity<?> deleteAccount(@PathVariable Long donorId, @AuthenticationPrincipal CustomUserDetails u) {
		checkAllowedToEdit(donorId, u.getUsername());
        try {
            bloodDonorService.deleteDonorAndDonations(donorId);
            return ResponseEntity.ok("Account deleted successfully");
        } catch (Exception e) {
            System.err.println("Error deleting account: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error deleting account");
        }
    }

	private void checkAllowedToEdit(Long id, String username) {
		String donorUsername = bloodDonorService.fetch(id).getUsername();
		if (!donorUsername.equals(username)) {
			throw new RequestDeniedException(
					"Only donor (" + donorUsername + ") can edit his profile, not: " + username
			);
		}
	}

}