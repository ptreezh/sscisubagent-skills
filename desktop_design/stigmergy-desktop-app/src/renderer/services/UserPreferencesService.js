// User Preferences Service
// This module manages user preferences and settings

const PREFERENCES_STORAGE_KEY = 'stigmergyUserPreferences';

class UserPreferencesService {
  /**
   * Default preferences
   */
  defaultPreferences = {
    theme: 'light',
    language: 'zh-CN',
    autoSave: true,
    notifications: true,
    commandHistory: true,
    filePreview: true,
    autoUpdate: true
  };

  /**
   * Get user preferences
   * @returns {Object} - User preferences
   */
  getPreferences() {
    try {
      const savedPreferences = localStorage.getItem(PREFERENCES_STORAGE_KEY);
      if (savedPreferences) {
        return { ...this.defaultPreferences, ...JSON.parse(savedPreferences) };
      }
      return this.defaultPreferences;
    } catch (error) {
      console.error('Failed to load preferences:', error);
      return this.defaultPreferences;
    }
  }

  /**
   * Save user preferences
   * @param {Object} preferences - Preferences to save
   * @returns {boolean} - Success status
   */
  savePreferences(preferences) {
    try {
      const mergedPreferences = { ...this.defaultPreferences, ...preferences };
      localStorage.setItem(PREFERENCES_STORAGE_KEY, JSON.stringify(mergedPreferences));
      return true;
    } catch (error) {
      console.error('Failed to save preferences:', error);
      return false;
    }
  }

  /**
   * Update a specific preference
   * @param {string} key - Preference key
   * @param {*} value - Preference value
   * @returns {boolean} - Success status
   */
  updatePreference(key, value) {
    const preferences = this.getPreferences();
    preferences[key] = value;
    return this.savePreferences(preferences);
  }

  /**
   * Reset preferences to default
   * @returns {boolean} - Success status
   */
  resetToDefault() {
    try {
      localStorage.setItem(PREFERENCES_STORAGE_KEY, JSON.stringify(this.defaultPreferences));
      return true;
    } catch (error) {
      console.error('Failed to reset preferences:', error);
      return false;
    }
  }

  /**
   * Get a specific preference value
   * @param {string} key - Preference key
   * @param {*} defaultValue - Default value if not found
   * @returns {*} - Preference value
   */
  getPreference(key, defaultValue = null) {
    const preferences = this.getPreferences();
    return preferences[key] !== undefined ? preferences[key] : defaultValue;
  }
}

// Export a singleton instance
module.exports = new UserPreferencesService();