
// Combine all data sources
let data = [
  ...window.CALCULATION,
  ...window.PARAMETER,
  ...window.VISIBILITY,
  ...window.INPUT,
  ...window.HOLDING
];

const tableBody = document.querySelector("#table tbody");
const filterFields = [...document.querySelectorAll("thead input")];

// Regex filter function
function matchesFilters(item) {
  const fields = {
      category: f_category.value.trim(),
      index: f_index.value.trim(),
      name: f_name.value.trim(),
      lsb: f_lsb.value.trim(),
      width: f_width.value.trim(),
      class: f_class.value.trim(),
      unit: f_unit.value.trim(),
      writeable: f_writeable.value.trim(),
      since: f_since.value.trim(),
      until: f_until.value.trim(),
      description: f_description.value.trim()
  };

  for (const key in fields) {
      const filterValue = fields[key];
      if (!filterValue) continue;

      try {
          const regex = new RegExp(filterValue, "i");
          if (!regex.test(String(item[key]))) return false;
      } catch (e) {
          return false; // invalid Regex -> no match
      }
  }

  return true;
}

// hide or show columns
function activateColumnToggle() {
  document.querySelectorAll('#columnToggle input').forEach(cb => {
      cb.addEventListener('change', () => {
          const colIndex = parseInt(cb.dataset.col);

          document.querySelectorAll(`thead tr th:nth-child(${colIndex})`)
              .forEach(th => th.classList.toggle('hide-col', !cb.checked));

          document.querySelectorAll(`tbody tr td:nth-child(${colIndex})`)
              .forEach(td => td.classList.toggle('hide-col', !cb.checked));
      });
  });
}

// initial visibility
function applyInitialColumnVisibility() {
  document.querySelectorAll('#columnToggle input').forEach(cb => {
      const colIndex = parseInt(cb.dataset.col);

      if (!cb.checked) {
          document.querySelectorAll(`thead tr th:nth-child(${colIndex})`)
              .forEach(th => th.classList.add('hide-col'));

          document.querySelectorAll(`tbody tr td:nth-child(${colIndex})`)
              .forEach(td => td.classList.add('hide-col'));
      }
  });
}

// Re-render table
function renderTable() {
  tableBody.innerHTML = "";

  data.filter(matchesFilters).forEach(item => {
      const row = document.createElement("tr");
      row.innerHTML = `
      <td>${item.category}</td>
      <td>${item.index}</td>
      <td>${item.name}</td>
      <td>${item.lsb}</td>
      <td>${item.width}</td>
      <td>${item.class}</td>
      <td>${item.unit}</td>
      <td>${item.writeable}</td>
      <td>${item.since}</td>
      <td>${item.until}</td>
      <td class="description">${item.description}</td>
      `;
      tableBody.appendChild(row);
  });

  applyInitialColumnVisibility();
}

// activate filter event
filterFields.forEach(f => f.addEventListener("input", renderTable));

// set creation-date
document.getElementById("createdInfo").textContent =
    `Generated automatically on ${window.META.createdOn}`;
// set version
document.getElementById("versionInfo").textContent =
    `Build version: ${window.META.version}`;



// initial rendering
activateColumnToggle();
renderTable();
