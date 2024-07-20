/**
 * Main JavaScript file for the example site
 * Handles dark/light mode toggle, lazy loading, and other client-side functionality
 */

/**
 * Utility function to build URLs by joining path segments and normalizing slashes
 * @param {string} baseUrl - The base URL
 * @param {...string} pathSegments - Path segments to join
 * @returns {string} - The normalized URL
 */
function buildUrl(baseUrl, ...pathSegments) {
  const segments = [baseUrl, ...pathSegments].filter(segment => segment);
  return segments.join('/').replace(/\/\/+/g, '/');
}

document.addEventListener('DOMContentLoaded', function() {
  // Initialize components
  initDarkModeToggle();
  initLazyLoading();
  enhanceCodeBlocks();
  initExternalLinks();
  initInfiniteScroll();
  initShareCopyButtons();
  initShareMenuToggle();
  initSiteInfoModal();
});

/**
 * Render a single article preview card (used everywhere for dynamic article lists)
 * @param {Object} article - Article metadata object (from index.json)
 * @returns {HTMLElement} - The article card element
 */
function renderArticleCard(article) {
  const articleElement = document.createElement('article');
  articleElement.className = 'post-card';

  // Construct base URL path
  const baseUrl = window.baseUrl || ''; // Get base URL from global var
  const articleUrl = buildUrl(baseUrl, article.url);
  const blogUrl = buildUrl(baseUrl, 'blog');

  // Format date nicely (e.g., Apr 17, 2025) - requires date parsing
  let formattedDate = '';
  if (article.written) {
    try {
      // More reliable parsing for YYYY-MM-DD format
      const parts = article.written.split('-');
      if (parts.length === 3) {
        const year = parseInt(parts[0], 10);
        const monthIndex = parseInt(parts[1], 10) - 1; // Month is 0-indexed
        const day = parseInt(parts[2], 10);
        const dateObj = new Date(Date.UTC(year, monthIndex, day)); // Use UTC to avoid timezone issues

        if (!isNaN(dateObj.getTime())) { // Check if the date is valid
          // Use client's default locale by omitting the locale argument
          formattedDate = dateObj.toLocaleDateString(undefined, { // <-- Use undefined for default locale
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            timeZone: 'UTC' // Keep UTC for consistency across timezones
          });
        } else {
           throw new Error('Invalid date components');
        }
      } else {
        throw new Error('Invalid date format');
      }
    } catch (e) {
      console.warn(`Could not parse date: ${article.written}`, e);
      formattedDate = article.written; // Fallback to original string
    }
  }

  // Generate topic links
  let topicsHtml = '';
  if (Array.isArray(article.topics)) {
    topicsHtml = article.topics.map(topic => {
      // Link to the blog page with the topic query parameter, respecting base URL
      return `<a href="${blogUrl}?topic=${topic}" class="post-topic" data-topic="${topic}">${topic}</a>`;
    }).join('');
  }

  // Construct inner HTML based on blog_index.html structure
  articleElement.innerHTML = `
    <div class="post-card-content">
        <h3><a href="${articleUrl}">${article.title}</a></h3>
        <div class="post-meta">
            <time datetime="${article.written || ''}">${formattedDate}</time>
            ${topicsHtml ? `<div class="post-topics">${topicsHtml}</div>` : ''}
        </div>
        ${article.description ? `<p class="post-excerpt">${article.description}</p>` : ''}        
    </div>
  `;

  return articleElement;
}
window.renderArticleCard = renderArticleCard;

/**
 * Initialize dark mode toggle functionality
 */
function initDarkModeToggle() {
  const themeToggle = document.getElementById('theme-toggle');
  if (!themeToggle) return;

  // Add light-mode class by default if no preference is stored
  if (!localStorage.getItem('theme')) {
    document.documentElement.classList.add('light-mode');
  }

  // Check for saved theme preference
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    document.documentElement.classList.remove('light-mode');
    document.documentElement.classList.add('dark-mode');
  } else {
    document.documentElement.classList.add('light-mode');
    document.documentElement.classList.remove('dark-mode');
  }

  themeToggle.addEventListener('click', function() {
    document.documentElement.classList.toggle('light-mode');
    document.documentElement.classList.toggle('dark-mode');
    
    // Save preference to localStorage
    const isDarkMode = document.documentElement.classList.contains('dark-mode');
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
  });
}

/**
 * Initialize lazy loading for images and iframes
 */
function initLazyLoading() {
  // Use native lazy loading if supported by the browser
  if ('loading' in HTMLImageElement.prototype) {
    const lazyImages = document.querySelectorAll('img[data-src]');
    lazyImages.forEach(img => {
      img.src = img.dataset.src;
    });
  } else {
    // Fallback using IntersectionObserver for older browsers
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            observer.unobserve(img);
          }
        });
      });
      
      lazyImages.forEach(img => imageObserver.observe(img));
    } else {
      // Ultimate fallback: load all images immediately
      lazyImages.forEach(img => {
        img.src = img.dataset.src;
      });
    }
  }
}

/**
 * Enhance code blocks with copy button
 */
function enhanceCodeBlocks() {
  const codeBlocks = document.querySelectorAll('pre code');
  
  codeBlocks.forEach(block => {
    const pre = block.parentNode;
    const copyButton = document.createElement('button');
    copyButton.className = 'copy-button';
    copyButton.textContent = 'Copy';
    
    copyButton.addEventListener('click', function() {
      const code = block.textContent;
      navigator.clipboard.writeText(code).then(() => {
        copyButton.textContent = 'Copied!';
        setTimeout(() => { copyButton.textContent = 'Copy'; }, 2000);
      }).catch(err => {
        console.error('Failed to copy: ', err);
        copyButton.textContent = 'Failed!';
        setTimeout(() => { copyButton.textContent = 'Copy'; }, 2000);
      });
    });
    
    pre.style.position = 'relative';
    copyButton.style.position = 'absolute';
    copyButton.style.right = '5px';
    copyButton.style.top = '5px';
    copyButton.style.padding = '3px 10px';
    copyButton.style.fontSize = '12px';
    copyButton.style.backgroundColor = 'var(--color-background)';
    copyButton.style.border = '1px solid var(--color-border)';
    copyButton.style.borderRadius = '4px';
    copyButton.style.cursor = 'pointer';
    copyButton.style.opacity = '0.7';
    
    copyButton.addEventListener('mouseenter', function() {
      this.style.opacity = '1';
    });
    
    copyButton.addEventListener('mouseleave', function() {
      this.style.opacity = '0.7';
    });
    
    pre.appendChild(copyButton);
  });
}

/**
 * Add noopener and noreferrer to external links
 */
function initExternalLinks() {
  const links = document.querySelectorAll('a[href^="http"]');
  
  links.forEach(link => {
    if (!link.hasAttribute('rel')) {
      link.setAttribute('rel', 'noopener noreferrer');
    } else if (!link.getAttribute('rel').includes('noopener')) {
      link.setAttribute('rel', link.getAttribute('rel') + ' noopener noreferrer');
    }
    
    // Open external links in new tab if not already specified
    if (!link.hasAttribute('target')) {
      link.setAttribute('target', '_blank');
    }
  });
}

/**
 * Initialize viewport-aware article loading with infinite scroll and topic filtering.
 */
function initInfiniteScroll() {
  // --- DOM Elements ---
  const postGrid = document.getElementById('post-grid');
  const loadingIndicator = document.getElementById('loading-indicator');
  const featuredPostsSection = document.querySelector('.featured-posts'); // Home page check
  
  // Blog page specific elements (may not exist on home page)
  const showTopicFiltersBtn = document.getElementById('show-topic-filters');
  const topicFiltersDiv = document.getElementById('topic-filters');
  const topicToggles = document.querySelectorAll('#topic-filters .topic-toggle'); // Only select toggles within the filter area
  const clearSelectionButton = document.getElementById('clear-topic-selection');
  const noResultsDiv = document.getElementById('no-results');
  const resetFiltersBtn = document.getElementById('reset-filters');

  // Only run if we have a post grid container
  if (!postGrid) return;

  // --- State ---
  let allArticles = []; // Full index from index.json
  let filteredArticleIndex = null; // Filtered index based on selected topics
  let currentIndexInDisplay = 0; // Tracks how many articles are currently *shown* in the grid
  let isLoading = false;
  let articlesPerBatch = 10; // Default batch size for loading
  let buffer = 2; // Viewport buffer (used in calculation)
  let resizeTimeout = null;
  let selectedTopics = new Set();
  const baseUrl = window.baseUrl || ''; // Get base URL

  // --- Initialization ---
  async function init() {
    try {
      if (loadingIndicator) loadingIndicator.style.display = 'block';

      // Construct fetch URL respecting base URL
      const indexUrl = buildUrl(baseUrl, 'content', 'index.json');
      const response = await fetch(indexUrl);
      if (!response.ok) throw new Error('Failed to load article index');
      allArticles = await response.json();

      if (featuredPostsSection) {
        // --- Home Page Logic --- 
        loadMoreArticles(3); // Load only the first 3
        if (loadingIndicator) loadingIndicator.style.display = 'none';
      } else {
        // --- Blog/Other Page Logic --- 
        articlesPerBatch = calculateArticlesForViewport();
        setupBlogPageListeners(); // Setup filtering and scroll listeners
        
        // Check for topic parameter in URL
        const urlParams = new URLSearchParams(window.location.search);
        const topicFromUrl = urlParams.get('topic');
        
        if (topicFromUrl) {
            // Find the corresponding toggle button and simulate a click
            const filterToggleButton = document.querySelector(`#topic-filters .topic-toggle[data-topic="${topicFromUrl}"]`);
            if (filterToggleButton) {
                // Ensure filters are visible before clicking
                if (topicFiltersDiv && topicFiltersDiv.style.display === 'none') {
                    showTopicFiltersBtn.click(); // Show the filter section
                }
                filterToggleButton.click(); // Apply the filter
            } else {
                // If topic from URL doesn't exist, load initial batch normally
                loadMoreArticles(articlesPerBatch);
            }
        } else {
            // No topic in URL, load initial batch normally
            loadMoreArticles(articlesPerBatch);
        }
      }

    } catch (error) {
      console.error('Error initializing article loading:', error);
      if (loadingIndicator) loadingIndicator.style.display = 'none';
      postGrid.innerHTML = '<p class="error-message">Failed to load articles. Please try again later.</p>';
    }
  }

  // --- Blog Page Specific Functions ---

  function setupBlogPageListeners() {
    // Filter UI Toggles
    if (showTopicFiltersBtn && topicFiltersDiv) {
        showTopicFiltersBtn.addEventListener('click', () => {
            const isHidden = topicFiltersDiv.style.display === 'none';
            topicFiltersDiv.style.display = isHidden ? 'flex' : 'none';
            showTopicFiltersBtn.textContent = isHidden ? 'Hide Filters' : 'Filter by Topic';
        });
    }

    // Topic Selection Toggles
    topicToggles.forEach(toggle => {
        toggle.addEventListener('click', handleTopicToggle);
    });

    // Clear/Reset Buttons
    if (clearSelectionButton) clearSelectionButton.addEventListener('click', clearTopicFilters);
    if (resetFiltersBtn) resetFiltersBtn.addEventListener('click', clearTopicFilters);

    // Infinite Scroll & Resize
    window.addEventListener('scroll', handleScroll);
    window.addEventListener('resize', handleResize);
    
    // Add listener for topic clicks within rendered cards (delegated to postGrid)
    postGrid.addEventListener('click', handleArticleTopicClick);
  }
  
  function handleArticleTopicClick(event) {
      // Check if the clicked element is a topic link within an article card
      if (event.target.matches('.post-card .post-topic[data-topic]')) {
          event.preventDefault(); // Prevent navigating to the topic page immediately
          const topic = event.target.dataset.topic;
          
          // Find the corresponding filter toggle button and simulate a click
          const filterToggleButton = document.querySelector(`#topic-filters .topic-toggle[data-topic="${topic}"]`);
          if (filterToggleButton) {
              filterToggleButton.click(); // This will trigger handleTopicToggle
          }
      }
  }

  function handleTopicToggle() {
    const topic = this.dataset.topic;
    if (selectedTopics.has(topic)) {
        selectedTopics.delete(topic);
        this.classList.remove('selected');
    } else {
        selectedTopics.add(topic);
        this.classList.add('selected');
    }
    updateSelectedTopicsDisplay();
    resetArticleDisplay();
  }

  function clearTopicFilters() {
    selectedTopics.clear();
    topicToggles.forEach(toggle => toggle.classList.remove('selected'));
    updateSelectedTopicsDisplay(); // Hides the display and clear button
    resetArticleDisplay();
    // Update the URL to remove the topic parameter if it exists
    const currentUrl = new URL(window.location.href);
    if (currentUrl.searchParams.has('topic')) {
        currentUrl.searchParams.delete('topic');
        // Use pushState to change URL without reload and allow back navigation
        history.pushState({}, '', currentUrl.toString())
    }
  }

  function updateSelectedTopicsDisplay() {    
    if (!clearSelectionButton) return; 
    
    if (selectedTopics.size === 0) {
        clearSelectionButton.style.display = 'none';
    } else {
        clearSelectionButton.style.display = 'block';
    }
    // Also update selection state on topic links within rendered cards
    postGrid.querySelectorAll('.post-topic[data-topic]').forEach(link => {
        if (selectedTopics.has(link.dataset.topic)) {
            link.classList.add('selected');
        } else {
            link.classList.remove('selected');
        }
    });
  }

  function resetArticleDisplay() {
    postGrid.innerHTML = '';
    currentIndexInDisplay = 0;
    filteredArticleIndex = null; // Reset filter
    if (noResultsDiv) noResultsDiv.style.display = 'none'; // Hide no results message

    if (selectedTopics.size > 0) {
        filteredArticleIndex = allArticles.filter(article => 
            article.topics && [...selectedTopics].every(topic => article.topics.includes(topic))
        );
        if (filteredArticleIndex.length === 0 && noResultsDiv) {
            noResultsDiv.style.display = 'block';
            return; // Don't load anything if no results
        }
    } 
    // If no topics selected or filter resulted in matches, load articles
    loadMoreArticles(); 
  }

  // --- Core Loading & Rendering Logic ---

  function calculateArticlesForViewport() {
    const viewportHeight = window.innerHeight;
    const viewportWidth = window.innerWidth;
    let articleHeight = 250; 
    let articlesPerRow = 1;
    const existingArticle = postGrid.querySelector('.post-card');
    if (existingArticle) {
      articleHeight = existingArticle.offsetHeight;
      const containerWidth = postGrid.offsetWidth;
      const articleWidth = existingArticle.offsetWidth;
      if (containerWidth && articleWidth) {
        articlesPerRow = Math.max(1, Math.floor(containerWidth / articleWidth));
      }
    } else {
      if (viewportWidth > 1200) articlesPerRow = 3;
      else if (viewportWidth > 768) articlesPerRow = 2;
      else articlesPerRow = 1;
    }
    const rowsInViewport = Math.ceil(viewportHeight / articleHeight);
    const viewportArticles = rowsInViewport * articlesPerRow;
    const totalArticlesToLoad = viewportArticles + (buffer * articlesPerRow);
    return Math.max(totalArticlesToLoad, 4);
  }

  function loadMoreArticles(count = articlesPerBatch) {
    const sourceIndex = filteredArticleIndex !== null ? filteredArticleIndex : allArticles;
    
    if (isLoading || currentIndexInDisplay >= sourceIndex.length) return;
    isLoading = true;
    if (loadingIndicator) loadingIndicator.style.display = 'block';

    try {
      const endIndex = Math.min(currentIndexInDisplay + count, sourceIndex.length);
      const articlesToLoad = sourceIndex.slice(currentIndexInDisplay, endIndex);

      articlesToLoad.forEach(article => {
        if (typeof window.renderArticleCard === 'function') {
            const card = window.renderArticleCard(article);
            postGrid.appendChild(card);
        } else {
            const el = document.createElement('article');
            // Construct fallback URL respecting base URL
            const fallbackUrl = buildUrl(baseUrl, article.url);
            el.innerHTML = `<a href="${fallbackUrl}"><h2>${article.title}</h2></a>`;
            postGrid.appendChild(el);
        }
      });
      
      currentIndexInDisplay = endIndex; // Update displayed count
      updateSelectedTopicsDisplay(); // Ensure new cards reflect current filter selection

      // Stop scroll listener if all articles from the current index (filtered or full) are loaded
      if (currentIndexInDisplay >= sourceIndex.length && !featuredPostsSection) {
        window.removeEventListener('scroll', handleScroll);
      }
    } catch (error) {
      console.error('Error rendering articles:', error);
    } finally {
      isLoading = false;
      if (loadingIndicator) loadingIndicator.style.display = 'none';
    }
  }

  function handleScroll() {
    // Use the currently active index (filtered or all) to check if more can be loaded
    const sourceIndex = filteredArticleIndex !== null ? filteredArticleIndex : allArticles;
    if (currentIndexInDisplay >= sourceIndex.length) return; // Don't try to load if all are displayed

    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
    const scrollThreshold = Math.min(scrollHeight - clientHeight - 300, scrollHeight * 0.75);
    
    if (scrollTop > scrollThreshold && !isLoading) {
      loadMoreArticles();
    }
  }

  function handleResize() {
    if (resizeTimeout) clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
      const newBatchSize = calculateArticlesForViewport();
      // Only log if the size changes, no need to reload existing ones
      if (newBatchSize !== articlesPerBatch) {
          console.log(`Viewport resized, will load ${newBatchSize} articles per batch on next load`);
          articlesPerBatch = newBatchSize;
      }
      // No automatic reload on resize, only affects future loads via scroll
    }, 250);
  }

  // --- Start Initialization ---
  init();
}

/**
 * Add copy-to-clipboard functionality for share link buttons
 */
function initShareCopyButtons() {
  document.querySelectorAll('.copy-link-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      const url = btn.getAttribute('data-url');
      if (!url) return;
      navigator.clipboard.writeText(url).then(function() {
        // Temporarily change the title for native tooltip feedback
        const originalTitle = btn.title;
        btn.title = 'Copied!';
        btn.blur(); // Hide tooltip if open
        setTimeout(function() {
          btn.title = originalTitle;
        }, 1500);
      }, function() {
        const originalTitle = btn.title;
        btn.title = 'Failed!';
        btn.blur();
        setTimeout(function() {
          btn.title = originalTitle;
        }, 1500);
      });
    });
  });
}

/**
 * Initialize share menu toggle functionality
 */
function initShareMenuToggle() {
  const toggleBtns = document.querySelectorAll('.share-toggle-btn');
  toggleBtns.forEach(function(toggleBtn) {
    const menuId = toggleBtn.getAttribute('aria-controls');
    if (!menuId) return;
    const menu = document.getElementById(menuId);
    if (!menu) return;
    // Hide menu by default
    menu.classList.remove('share-menu-open');
    toggleBtn.setAttribute('aria-expanded', 'false');
    // Toggle menu on click
    toggleBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      const expanded = menu.classList.toggle('share-menu-open');
      toggleBtn.setAttribute('aria-expanded', expanded ? 'true' : 'false');
    });
    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
      if (!menu.classList.contains('share-menu-open')) return;
      if (!menu.contains(e.target) && e.target !== toggleBtn) {
        menu.classList.remove('share-menu-open');
        toggleBtn.setAttribute('aria-expanded', 'false');
      }
    });
    // Keyboard accessibility: close on Escape
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        menu.classList.remove('share-menu-open');
        toggleBtn.setAttribute('aria-expanded', 'false');
      }
    });
  });
}

/**
 * Initialize site info modal functionality
 */
function initSiteInfoModal() {
  const siteInfoToggle = document.getElementById('site-info-toggle');
  const siteInfoModal = document.getElementById('site-info-modal');
  const siteInfoClose = document.getElementById('site-info-close');

  if (!siteInfoToggle || !siteInfoModal) return;

  siteInfoToggle.addEventListener('click', (e) => {
    e.preventDefault();
    siteInfoModal.style.display = 'flex';
  });

  if (siteInfoClose) {
    siteInfoClose.addEventListener('click', (e) => {
      e.preventDefault();
      siteInfoModal.style.display = 'none';
    });
  }

  // Close modal when clicking outside content
  siteInfoModal.addEventListener('click', (e) => {
    if (e.target === siteInfoModal) {
      siteInfoModal.style.display = 'none';
    }
  });

  // Close modal with Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && siteInfoModal.style.display === 'flex') {
      siteInfoModal.style.display = 'none';
    }
  });
}