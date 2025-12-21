// Data Persistence Service
// This module handles data storage and retrieval for the application

const DATA_STORAGE_KEY = 'stigmergyAppData';

class DataPersistenceService {
  /**
   * Save application data to localStorage
   * @param {Object} data - Data to save
   * @returns {boolean} - Success status
   */
  saveData(data) {
    try {
      const serializedData = JSON.stringify(data);
      localStorage.setItem(DATA_STORAGE_KEY, serializedData);
      return true;
    } catch (error) {
      console.error('Failed to save data:', error);
      return false;
    }
  }

  /**
   * Load application data from localStorage
   * @returns {Object|null} - Loaded data or null if not found
   */
  loadData() {
    try {
      const serializedData = localStorage.getItem(DATA_STORAGE_KEY);
      if (serializedData) {
        return JSON.parse(serializedData);
      }
      return null;
    } catch (error) {
      console.error('Failed to load data:', error);
      return null;
    }
  }

  /**
   * Save skills data
   * @param {Array} skills - Skills array to save
   * @returns {boolean} - Success status
   */
  saveSkills(skills) {
    const appData = this.loadData() || {};
    appData.skills = skills;
    return this.saveData(appData);
  }

  /**
   * Load skills data
   * @returns {Array} - Skills array or empty array if not found
   */
  loadSkills() {
    const appData = this.loadData();
    return appData && appData.skills ? appData.skills : [];
  }

  /**
   * Save projects data
   * @param {Array} projects - Projects array to save
   * @returns {boolean} - Success status
   */
  saveProjects(projects) {
    const appData = this.loadData() || {};
    appData.projects = projects;
    return this.saveData(appData);
  }

  /**
   * Load projects data
   * @returns {Array} - Projects array or empty array if not found
   */
  loadProjects() {
    const appData = this.loadData();
    return appData && appData.projects ? appData.projects : [];
  }

  /**
   * Save user preferences
   * @param {Object} preferences - User preferences to save
   * @returns {boolean} - Success status
   */
  savePreferences(preferences) {
    const appData = this.loadData() || {};
    appData.preferences = preferences;
    return this.saveData(appData);
  }

  /**
   * Load user preferences
   * @returns {Object} - User preferences or empty object if not found
   */
  loadPreferences() {
    const appData = this.loadData();
    return appData && appData.preferences ? appData.preferences : {};
  }

  /**
   * Clear all application data
   * @returns {boolean} - Success status
   */
  clearAllData() {
    try {
      localStorage.removeItem(DATA_STORAGE_KEY);
      return true;
    } catch (error) {
      console.error('Failed to clear data:', error);
      return false;
    }
  }
}

// Export a singleton instance
module.exports = new DataPersistenceService();