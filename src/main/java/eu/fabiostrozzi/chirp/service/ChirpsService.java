// ChirpsService.java, created on Jan 17, 2013
package eu.fabiostrozzi.chirp.service;

import java.util.List;

import eu.fabiostrozzi.chirp.model.Chirp;
import eu.fabiostrozzi.chirp.model.User;

/**
 * @author fabio
 * 
 */
public interface ChirpsService {

    /**
     * @param user
     * @return
     */
    List<User> getFollowingOf(String user);

    /**
     * @param user
     * @return
     */
    List<User> getFollowersOf(String user);

    /**
     * @param user
     * @return
     */
    List<Chirp> getChirpsOf(String user);

    /**
     * @param user
     * @param key
     * @return
     */
    List<Chirp> searchChirpsOf(String user, String key);

    /**
     * @param user
     * @return
     */
    boolean userExists(String user);

    /**
     * @param actor
     * @param friend
     */
    void follow(String actor, String friend);

    /**
     * @param actor
     * @param who
     */
    void unfollow(String actor, String who);

    /**
     * @param token
     * @return
     */
    boolean isValidToken(String token);

    /**
     * @param token
     * @return
     */
    String getUserByToken(String token);
}
