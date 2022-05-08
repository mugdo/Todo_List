from django.test import TestCase



#  git command for reset github code
# git stash


csrf = '{{ csrf_token }}';
    function save_term_and_policy () {
        console.log('Enter');
        let title = $('#term_and_policy_title').val();
        let content = $('#footer_term_and_policy').val();
        if (!title) toastr.error('Titile field is required!');
        else if (!content) toastr.error('Content field is required!');
        else {
            formData = new FormData()
            formData.append('title', title);
            formData.append('content', content);
            formData.append('csrfmiddlewaretoken', csrf);
            
            let url = "{% url 'dashboard:footer_term_and_policy_content_save_url' %}";

            $.ajax({
                url: url,
                data: formData,
                type: "POST",
                processData: false,
                contentType: false,
                success: function (data) {
                    $('#term_and_policy_content_update_'+ data.id).summernote();
                    $("#term_and_policy_modal").modal('toggle');
                    toastr.success('Saved successfully');
                    $('#term_and_policy_table').append(
                        `<tr id="term_and_policy_`+data.id+`">
                            <td>`+data.id+`</td>
                            <td>`+title+`</td>
                            <td>`+data.slug+`</td>
                            <td>
                                <button style="font-size:24px; " class="far fa-edit" onclick="update_term_and_policy(`+ data.id +`)"></button>
                            </td>
                            <td>
                                <button style="font-size:24px;" class="far fa-trash-alt" onclick="delete_term_and_policy(`+ data.id +`)"></button>
                            </td>
                        </tr>`
                    );
                },
                error: function (data) {
                    console.log(data);
                }
            });
        }
    }