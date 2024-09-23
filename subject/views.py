from django.shortcuts import render, get_object_or_404, redirect
from .models import Subject, Material
from .forms import SubjectForm, MaterialUploadForm
from module_group.models import ModuleGroup
from django.http import HttpResponse
from django.contrib import messages
import zipfile
import os

# Subject list view
def subject_list(request):
    module_groups = ModuleGroup.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {
        'module_groups': module_groups,
        'subjects': subjects,
    })

# Add a new subject
def subject_add(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added successfully.')
            return redirect('subject:subject_list')
        else:
            messages.error(request, 'Failed to add subject. Please check the form for errors.')
    else:
        form = SubjectForm()
    
    return render(request, 'subject_form.html', {'form': form})

# Edit a subject
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully.')
            return redirect('subject:subject_list')
        else:
            messages.error(request, 'Failed to update subject. Please check the form for errors.')
    else:
        form = SubjectForm(instance=subject)
    
    return render(request, 'subject_form.html', {'form': form})

# Delete a subject
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully.')
        return redirect('subject:subject_list')
    
    return render(request, 'subject_confirm_delete.html', {'subject': subject})

# Delete material
def delete_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    subject = material.subject  # Assuming material has a ForeignKey to subject
    if request.method == 'POST':
        material.delete()
        messages.success(request, 'Material deleted successfully.')
    return redirect('subject:subject_materials', subject_id=subject.pk)


def upload_material(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        subject = get_object_or_404(Subject, pk=subject_id)
        material_type = request.POST['material_type']
        
        files = request.FILES.getlist('file')
        
        for file in files:
            material = Material(file=file, subject=subject, material_type=material_type)
            material.save()

        messages.success(request, 'Materials uploaded successfully.')
        return redirect('subject:subject_materials', subject_id=subject.pk)

    subjects = Subject.objects.all()
    form = MaterialUploadForm()  # Create an instance of the form
    return render(request, 'materials/upload_materials.html', {
        'subjects': subjects,
        'form': form,  # Pass the form to the template
    })


# Display materials by subject view
def subject_materials(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    assignments = subject.materials.filter(material_type='assignments')
    labs = subject.materials.filter(material_type='labs')
    lectures = subject.materials.filter(material_type='lectures')
    
    return render(request, 'materials/subject_materials.html', {
        'subject': subject,
        'assignments': assignments,
        'labs': labs,
        'lectures': lectures,
    })


def download_all_materials(request, material_type):
    zip_filename = f'{material_type}s.zip'
    
    # Create a zip file
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        materials = Material.objects.filter(material_type=material_type)  # Use 'material_type' instead of 'type'
        for material in materials:
            zip_file.write(material.file.path, arcname=os.path.basename(material.file.name))

    # Serve the zip file
    response = HttpResponse(open(zip_filename, 'rb'), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'
    
    # Optionally, delete the zip file after sending it
    # os.remove(zip_filename)
    
    return response


