
async function getUserData(){
    const response = await fetch('/api/users');
    return response.json();
}

function loadTable(users){
    const table = document.querySelector('#result');
    for(let user of users){
        table.innerHTML += `<tr>
            <td>${user.id}</td>
            <td>${user.username}</td>
        </tr>`;
    }
}

async function main(){
    const users = await getUserData();
    loadTable(users);
}

// Use EXERCISES as reference to WORKOUTS_DATA from backend
const EXERCISES = WORKOUTS_DATA || [];

// State
let currentView = 'browse';
let searchQuery = '';
let categoryFilter = 'All';
let currentRoutine = [];
let routineName = '';
let savedRoutines = ROUTINES_DATA || [];

// Get unique categories from database workouts
const categories = ['All', ...new Set(EXERCISES.map(e => e.category))];

// DOM Elements
const navButtons = document.querySelectorAll('.nav-btn');
const views = document.querySelectorAll('.view');
const searchInput = document.getElementById('searchInput');
const filterButtons = document.getElementById('filterButtons');
const exerciseGrid = document.getElementById('exerciseGrid');
const routinesGrid = document.getElementById('routinesGrid');
const routineNameInput = document.getElementById('routineNameInput');
const currentRoutineContent = document.getElementById('currentRoutineContent');

// Initialize
function init() {
    renderFilterButtons();
    renderExercises();
    renderRoutines();
    setupEventListeners();
}

// Setup Event Listeners
function setupEventListeners() {
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const view = btn.dataset.view;
            switchView(view);
        });
    });

    searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value;
        renderExercises();
    });

    routineNameInput.addEventListener('input', (e) => {
        routineName = e.target.value;
    });
}

// Switch View
function switchView(view) {
    currentView = view;

    navButtons.forEach(btn => {
        if (btn.dataset.view === view) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    views.forEach(v => {
        v.classList.remove('active');
    });

    document.getElementById(`${view}-view`).classList.add('active');

    if (view === 'create') {
        renderCurrentRoutine();
    }
}

// Render Filter Buttons
function renderFilterButtons() {
    filterButtons.innerHTML = categories.map(cat => `
        <button class="filter-btn ${cat === categoryFilter ? 'active' : ''}"
                onclick="setCategory('${cat}')">
            ${cat}
        </button>
    `).join('');
}

// Set Category Filter
function setCategory(category) {
    categoryFilter = category;
    renderFilterButtons();
    renderExercises();
}

// Filter Exercises
function getFilteredExercises() {
    return EXERCISES.filter(exercise => {
        const matchesSearch = exercise.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            exercise.muscleGroups.some(m => m.toLowerCase().includes(searchQuery.toLowerCase()));
        const matchesCategory = categoryFilter === 'All' || exercise.category === categoryFilter;
        return matchesSearch && matchesCategory;
    });
}

// Get a workout by ID from EXERCISES
function getWorkoutByName(name) {
    return EXERCISES.find(e => e.name === name);
}

// Render Exercises
function renderExercises() {
    const filtered = getFilteredExercises();

    exerciseGrid.innerHTML = filtered.map(exercise => `
        <div class="exercise-card" onclick="viewExerciseDetail('${exercise.id}')">
            <div class="exercise-image">
                <div class="exercise-image-icon">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                    </svg>
                </div>
                <p class="placeholder-text">[Exercise Image]</p>
            </div>
            <div class="exercise-content">
                <div class="exercise-header">
                    <div class="exercise-info">
                        <div class="exercise-name">${exercise.name}</div>
                        <div class="exercise-category">${exercise.category}</div>
                    </div>
                    <button class="add-btn" onclick="event.stopPropagation(); addToRoutine('${exercise.id}')">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                        </svg>
                    </button>
                </div>
                <div class="muscle-tags">
                    ${exercise.muscleGroups.map(muscle => `
                        <span class="muscle-tag">${muscle}</span>
                    `).join('')}
                </div>
                <div class="exercise-footer">
                    <p class="exercise-description">${exercise.description}</p>
                    <span class="difficulty-badge difficulty-${exercise.difficulty.toLowerCase()}">
                        ${exercise.difficulty}
                    </span>
                </div>
            </div>
        </div>
    `).join('');
}

// Add Exercise to Routine
function addToRoutine(exerciseId) {
    const exercise = EXERCISES.find(e => e.id === exerciseId);
    if (exercise) {
        currentRoutine.push({...exercise, workoutId: parseInt(exerciseId)});
        switchView('create');
        renderCurrentRoutine();
    }
}

// Remove from Routine
function removeFromRoutine(index) {
    currentRoutine.splice(index, 1);
    renderCurrentRoutine();
}

// Render Current Routine
function renderCurrentRoutine() {
    if (currentRoutine.length === 0) {
        currentRoutineContent.innerHTML = `
            <div class="empty-state">
                <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                <h3 class="empty-title">No exercises yet</h3>
                <p class="empty-description">Browse workouts to add exercises to your routine</p>
                <button class="btn-primary" onclick="switchView('browse')">Browse Workouts</button>
            </div>
        `;
    } else {
        currentRoutineContent.innerHTML = `
            <div class="current-routine-list">
                ${currentRoutine.map((exercise, index) => `
                    <div class="routine-list-item">
                        <span class="routine-item-number">${index + 1}</span>
                        <div class="routine-item-info">
                            <div class="routine-item-name">${exercise.name}</div>
                            <div class="routine-item-category">${exercise.category}</div>
                        </div>
                        <button class="remove-btn" onclick="removeFromRoutine(${index})">
                            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                            </svg>
                        </button>
                    </div>
                `).join('')}
            </div>
            <div class="action-buttons">
                <button class="btn-accent" onclick="saveRoutine()" ${!routineName.trim() ? 'disabled' : ''}>
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"/>
                    </svg>
                    Save Routine
                </button>
                <button class="btn-primary" onclick="switchView('browse')">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                    </svg>
                    Add More
                </button>
            </div>
        `;
    }
}

// API: Create Routine
async function createRoutineAPI(name, description) {
    try {
        const response = await fetch('/api/routines', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name,
                description: description || "",
            })
        });

        if (!response.ok) {
            throw new Error(`Failed to create routine: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error creating routine:', error);
        alert('Failed to create routine. Please try again.');
        throw error;
    }
}

// API: Add Workout to Routine
async function addWorkoutToRoutineAPI(routineId, workoutId, position, sets = 3, reps = 10) {
    try {
        const response = await fetch(`/api/routines/${routineId}/workouts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                workout_id: workoutId,
                position,
                sets,
                reps,
            })
        });

        if (!response.ok) {
            throw new Error(`Failed to add workout: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error adding workout to routine:', error);
        throw error;
    }
}

// API: Delete Routine
async function deleteRoutineAPI(routineId) {
    try {
        const response = await fetch(`/api/routines/${routineId}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error(`Failed to delete routine: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Error deleting routine:', error);
        alert('Failed to delete routine. Please try again.');
        throw error;
    }
}

// API: Fetch Routines for Current User (with full details)
async function fetchRoutinesAPI() {
    try {
        const response = await fetch('/api/routines');

        if (!response.ok) {
            throw new Error(`Failed to fetch routines: ${response.statusText}`);
        }

        const routines = await response.json();
        
        // Fetch full details for each routine (including workouts)
        const detailedRoutines = [];
        for (let routine of routines) {
            try {
                const detailResponse = await fetch(`/api/routines/${routine.id}`);
                if (detailResponse.ok) {
                    const detailed = await detailResponse.json();
                    detailedRoutines.push(detailed);
                } else {
                    detailedRoutines.push(routine);
                }
            } catch (error) {
                console.warn(`Could not fetch details for routine ${routine.id}:`, error);
                detailedRoutines.push(routine);
            }
        }
        
        return detailedRoutines;
    } catch (error) {
        console.error('Error fetching routines:', error);
        return [];
    }
}

// Save Routine (creates in database)
async function saveRoutine() {
    if (currentRoutine.length === 0 || !routineName.trim()) return;

    try {
        // Create routine in database
        const newRoutine = await createRoutineAPI(routineName, '');

        // Add each workout to the routine
        for (let i = 0; i < currentRoutine.length; i++) {
            const exercise = currentRoutine[i];
            await addWorkoutToRoutineAPI(newRoutine.id, parseInt(exercise.id), i);
        }

        // Refresh the routines list
        savedRoutines = await fetchRoutinesAPI();

        // Reset form
        currentRoutine = [];
        routineName = '';
        routineNameInput.value = '';

        renderRoutines();
        switchView('routines');
        alert('Routine saved successfully!');
    } catch (error) {
        console.error('Error saving routine:', error);
    }
}

// Delete Routine
async function deleteRoutine(routineId) {
    if (!confirm('Are you sure you want to delete this routine?')) return;

    try {
        await deleteRoutineAPI(routineId);
        savedRoutines = await fetchRoutinesAPI();
        renderRoutines();
    } catch (error) {
        console.error('Error deleting routine:', error);
    }
}

// Render Routines
function renderRoutines() {
    if (savedRoutines.length === 0) {
        routinesGrid.innerHTML = `
            <div class="empty-state" style="grid-column: 1 / -1;">
                <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/>
                </svg>
                <h3 class="empty-title">No routines saved</h3>
                <p class="empty-description">Create your first workout routine to get started</p>
                <button class="btn-accent" onclick="switchView('create')">Create Routine</button>
            </div>
        `;
    } else {
        routinesGrid.innerHTML = savedRoutines.map(routine => {
            const routineExercises = routine.routine_workouts || [];
            const categories = [...new Set(routineExercises.map(rw => rw.workout.category))];
            const totalExercises = routineExercises.length;

            return `
                <div class="routine-card">
                    <div class="routine-preview">
                        ${routineExercises.slice(0, 3).map(() => `
                            <div class="routine-preview-item">
                                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                </svg>
                            </div>
                        `).join('')}
                        ${totalExercises < 3 ? Array(3 - totalExercises).fill(0).map(() => `
                            <div class="routine-preview-item routine-preview-empty"></div>
                        `).join('') : ''}
                    </div>
                    <div class="routine-content">
                        <div class="routine-header">
                            <div class="routine-info">
                                <h3>${routine.name}</h3>
                                <p class="routine-count">${totalExercises} ${totalExercises === 1 ? 'exercise' : 'exercises'}</p>
                            </div>
                            <div class="routine-actions">
                                <button class="icon-btn btn-remix" onclick="editRoutine(${routine.id})" title="Edit routine">
                                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                                    </svg>
                                </button>
                                <button class="icon-btn btn-delete" onclick="deleteRoutine(${routine.id})" title="Delete routine">
                                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                                    </svg>
                                </button>
                            </div>
                        </div>
                        <div class="routine-exercises">
                            ${routineExercises.map((rw, idx) => `
                                <div class="routine-exercise-item">
                                    <span class="routine-exercise-number">${idx + 1}.</span>
                                    <span class="routine-exercise-name">${rw.workout.name}</span>
                                </div>
                            `).join('')}
                        </div>
                        <div class="category-tags">
                            ${categories.map(cat => `
                                <span class="category-tag">${cat}</span>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }
}

// View Exercise Detail Modal
function viewExerciseDetail(exerciseId) {
    const exercise = EXERCISES.find(e => e.id === exerciseId);
    if (exercise) {
        // Store current exercise ID for adding to routine
        window.currentExerciseId = exerciseId;
        
        // Populate modal with exercise data
        document.getElementById('modalExerciseName').textContent = exercise.name;
        document.getElementById('modalExerciseDescription').textContent = exercise.description;
        document.getElementById('modalExerciseMuscleGroup').textContent = exercise.category;
        document.getElementById('modalExerciseDifficulty').textContent = exercise.difficulty;
        document.getElementById('modalExerciseEquipment').textContent = exercise.equipment;
        document.getElementById('modalExerciseDifficultyDetail').textContent = exercise.difficulty;
        
        // Show modal
        document.getElementById('exerciseDetailModal').classList.add('active');
    }
}

// Close exercise detail modal
function closeExerciseModal() {
    document.getElementById('exerciseDetailModal').classList.remove('active');
    window.currentExerciseId = null;
}

// Add exercise from modal to routine
function addFromModalToRoutine() {
    if (window.currentExerciseId) {
        addToRoutine(window.currentExerciseId);
        closeExerciseModal();
    }
}

// Open edit routine modal
function editRoutine(routineId) {
    const routine = savedRoutines.find(r => r.id === routineId);
    if (!routine) return;
    
    // Store routine ID for saving
    window.editingRoutineId = routineId;
    
    // Populate form
    document.getElementById('editRoutineName').value = routine.name;
    document.getElementById('editRoutineDescription').value = routine.description || '';
    
    // Populate exercises list
    const exercisesList = document.getElementById('editRoutineExercisesList');
    if (routine.routine_workouts && routine.routine_workouts.length > 0) {
        exercisesList.innerHTML = routine.routine_workouts.map((rw, idx) => `
            <div class="edit-routine-exercise-item">
                <span style="color: #64748b;">${idx + 1}</span>
                <div class="edit-routine-exercise-name">${rw.workout.name}</div>
                <input type="number" value="${rw.sets}" placeholder="Sets" class="exercise-sets-input" data-rw-id="${rw.id}" min="1">
                <input type="number" value="${rw.reps}" placeholder="Reps" class="exercise-reps-input" data-rw-id="${rw.id}" min="1">
                <button type="button" class="edit-routine-remove-btn" onclick="removeExerciseFromEdit(${rw.id})">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                </button>
            </div>
        `).join('');
    } else {
        exercisesList.innerHTML = '<p style="color: #64748b;">No exercises in this routine</p>';
    }
    
    // Show modal
    document.getElementById('editRoutineModal').classList.add('active');
}

// Close edit routine modal
function closeEditRoutineModal() {
    document.getElementById('editRoutineModal').classList.remove('active');
    window.editingRoutineId = null;
}

// Remove exercise from edit form (local only)
function removeExerciseFromEdit(rwId) {
    const exerciseItem = document.querySelector(`.edit-routine-exercise-item [data-rw-id="${rwId}"]`).closest('.edit-routine-exercise-item');
    exerciseItem.remove();
}

// Save routine edits
async function saveRoutineEdits() {
    const routineId = window.editingRoutineId;
    const name = document.getElementById('editRoutineName').value.trim();
    const description = document.getElementById('editRoutineDescription').value.trim();
    
    if (!name) {
        alert('Please enter a routine name');
        return;
    }
    
    try {
        // Update routine metadata
        const response = await fetch(`/api/routines/${routineId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name,
                description,
            })
        });
        
        if (!response.ok) {
            throw new Error(`Failed to update routine: ${response.statusText}`);
        }
        
        // Update exercise sets/reps
        const setsInputs = document.querySelectorAll('.exercise-sets-input');
        const repsInputs = document.querySelectorAll('.exercise-reps-input');
        
        for (let input of setsInputs) {
            const rwId = parseInt(input.dataset.rwId);
            const sets = parseInt(input.value);
            await updateRoutineWorkoutAPI(routineId, rwId, { sets });
        }
        
        for (let input of repsInputs) {
            const rwId = parseInt(input.dataset.rwId);
            const reps = parseInt(input.value);
            await updateRoutineWorkoutAPI(routineId, rwId, { reps });
        }
        
        // Refresh data and close modal
        savedRoutines = await fetchRoutinesAPI();
        renderRoutines();
        closeEditRoutineModal();
        alert('Routine updated successfully!');
    } catch (error) {
        console.error('Error saving routine edits:', error);
        alert('Failed to save routine changes. Please try again.');
    }
}

// API: Update Routine Workout (sets/reps)
async function updateRoutineWorkoutAPI(routineId, rwId, data) {
    try {
        const response = await fetch(`/api/routines/${routineId}/workouts/${rwId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`Failed to update workout: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error updating routine workout:', error);
        throw error;
    }
}

// Close modals when clicking outside
document.addEventListener('click', (e) => {
    const exerciseModal = document.getElementById('exerciseDetailModal');
    const editModal = document.getElementById('editRoutineModal');
    
    if (e.target === exerciseModal) {
        closeExerciseModal();
    }
    if (e.target === editModal) {
        closeEditRoutineModal();
    }
});

// Initialize app
init();

main();