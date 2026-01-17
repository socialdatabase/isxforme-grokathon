<template>
  <div class="categories-container">
    <!-- Breadcrumb navigation -->
    <div class="breadcrumb" v-if="breadcrumbs.length > 0">
      <button class="breadcrumb-item" @click="goToLevel(0)">
        All Categories
      </button>
      <template v-for="(crumb, idx) in breadcrumbs" :key="crumb.id">
        <span class="breadcrumb-separator">›</span>
        <button 
          class="breadcrumb-item"
          :class="{ active: idx === breadcrumbs.length - 1 }"
          @click="goToLevel(Number(idx) + 1)"
        >
          {{ crumb.name }}
        </button>
      </template>
    </div>
    
    <p class="results-subtitle" v-else>
      Explore categories
    </p>
    
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <span>Loading categories...</span>
    </div>
    
    <div v-else-if="categories.length === 0" class="empty-state">
      <p>No subcategories found</p>
      <button class="back-btn" @click="goBack" v-if="breadcrumbs.length > 0">
        ← Go back
      </button>
    </div>
    
    <div v-else class="category-grid">
      <button
        v-for="category in categories"
        :key="category.id"
        class="category-btn"
        @click="selectCategory(category)"
      >
        {{ category.name }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Classifier {
  name: string
  parent_id: number | null
  group: string | null
  level: number
}

type ClassifiersData = Record<string, Classifier>

const classifiers = ref<ClassifiersData>({})
const categories = ref<{ id: string; name: string }[]>([])
const loading = ref(true)
const breadcrumbs = ref<{ id: string; name: string }[]>([])

// Categories to exclude from display
const excludedPrefixes = ['ALIAS FOR', 'No Path', 'Pro Sentiment', 'Retriever Test', 'Fossil Hunter']

const isValidCategory = (name: string): boolean => {
  return !excludedPrefixes.some(prefix => name.startsWith(prefix))
}

const loadClassifiers = async () => {
  loading.value = true
  try {
    const response = await fetch('/classifiers.json')
    classifiers.value = await response.json()
    showRootCategories()
  } catch (error) {
    console.error('Failed to load classifiers:', error)
    categories.value = []
  } finally {
    loading.value = false
  }
}

const showRootCategories = () => {
  // Get level 1 categories
  const entries = Object.entries(classifiers.value) as [string, Classifier][]
  const level1 = entries
    .filter(([_, v]) => v.level === 1 && isValidCategory(v.name))
    .map(([id, v]) => ({ id, name: v.name }))
    .sort((a, b) => a.name.localeCompare(b.name))
  categories.value = level1
}

const getChildren = (parentId: string): { id: string; name: string }[] => {
  const parentIdNum = parseInt(parentId)
  const entries = Object.entries(classifiers.value) as [string, Classifier][]
  return entries
    .filter(([_, v]) => v.parent_id === parentIdNum && isValidCategory(v.name))
    .map(([id, v]) => ({ id, name: v.name }))
    .sort((a, b) => a.name.localeCompare(b.name))
}

const selectCategory = (category: { id: string; name: string }) => {
  const children = getChildren(category.id)
  if (children.length > 0) {
    breadcrumbs.value.push(category)
    categories.value = children
  }
  // If no children, don't navigate (it's a leaf node)
}

const goToLevel = (level: number) => {
  if (level === 0) {
    // Go back to root
    breadcrumbs.value = []
    showRootCategories()
  } else {
    // Go to specific level
    breadcrumbs.value = breadcrumbs.value.slice(0, level)
    const parent = breadcrumbs.value[breadcrumbs.value.length - 1]
    categories.value = getChildren(parent.id)
  }
}

const goBack = () => {
  if (breadcrumbs.value.length > 0) {
    goToLevel(breadcrumbs.value.length - 1)
  }
}

onMounted(() => {
  loadClassifiers()
})
</script>

<style scoped>
.categories-container {
  width: 100%;
}

.breadcrumb {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.25rem;
  margin-bottom: 1.5rem;
  padding: 0.75rem 1rem;
  background: #16181c;
  border-radius: 8px;
}

.breadcrumb-item {
  background: none;
  border: none;
  color: #1d9bf0;
  font-size: 0.9rem;
  font-family: inherit;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  transition: background 0.15s ease;
}

.breadcrumb-item:hover {
  background: rgba(29, 155, 240, 0.1);
}

.breadcrumb-item.active {
  color: #e7e9ea;
  cursor: default;
}

.breadcrumb-item.active:hover {
  background: none;
}

.breadcrumb-separator {
  color: #71767b;
  font-size: 0.9rem;
}

.results-subtitle {
  font-size: 1rem;
  color: #71767b;
  text-align: center;
  margin-bottom: 1.5rem;
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 2rem;
  color: #71767b;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #2f3336;
  border-top-color: #1d9bf0;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  color: #71767b;
}

.back-btn {
  background: none;
  border: 1px solid #2f3336;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  color: #1d9bf0;
  font-size: 0.9rem;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s ease;
}

.back-btn:hover {
  background: #16181c;
  border-color: #1d9bf0;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.category-btn {
  background-color: transparent;
  border: 1px solid #2f3336;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  color: #e7e9ea;
  font-size: 0.95rem;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s ease;
  text-align: center;
}

.category-btn:hover {
  background-color: #16181c;
  border-color: #3f4347;
}

/* Responsive */
@media (max-width: 900px) {
  .category-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 600px) {
  .breadcrumb {
    padding: 0.5rem 0.75rem;
  }
  
  .breadcrumb-item {
    font-size: 0.85rem;
  }
  
  .category-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .category-btn {
    padding: 0.85rem 1rem;
    font-size: 0.9rem;
  }
}
</style>
